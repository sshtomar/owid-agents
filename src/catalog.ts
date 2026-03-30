import { readFileSync, writeFileSync, existsSync, mkdirSync, renameSync } from "node:fs";
import { dirname, join, resolve, basename } from "node:path";
import type {
  CatalogIndex,
  VizIndex,
  DatasetEntry,
  DatasetFile,
  VizEntry,
} from "./types.js";

const DATA_DIR = process.env.OWID_DATA_DIR ?? join(import.meta.dirname, "..", "data");
const CATALOG_DIR = join(DATA_DIR, "catalog");
const DATASETS_DIR = join(CATALOG_DIR, "datasets");
const VIZ_DIR = join(DATA_DIR, "visualizations");
const VIZ_FILES_DIR = join(VIZ_DIR, "viz");
const NOTEBOOKS_DIR = join(VIZ_DIR, "notebooks");

const CATALOG_INDEX = join(CATALOG_DIR, "index.json");
const VIZ_INDEX = join(VIZ_DIR, "index.json");

// --- ID validation ---

const SAFE_ID_PATTERN = /^[a-zA-Z0-9_-]+$/;

export function isValidId(id: string): boolean {
  return SAFE_ID_PATTERN.test(id) && id.length > 0 && id.length <= 200;
}

function assertValidId(id: string): void {
  if (!isValidId(id)) {
    throw new Error(`Invalid ID: "${id}" -- must match [a-zA-Z0-9_-]+`);
  }
}

// --- File helpers ---

function ensureDir(dir: string): void {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

function readJSON<T>(path: string, fallback: T): T {
  if (!existsSync(path)) return fallback;
  try {
    const raw = readFileSync(path, "utf-8");
    return JSON.parse(raw) as T;
  } catch (err) {
    console.error(`[catalog] Failed to parse JSON at ${path}:`, err instanceof Error ? err.message : err);
    return fallback;
  }
}

function writeJSON(path: string, data: unknown): void {
  ensureDir(dirname(path));
  const content = JSON.stringify(data, null, 2) + "\n";
  // Atomic write: write to temp file, then rename
  const tmpPath = path + ".tmp";
  writeFileSync(tmpPath, content, "utf-8");
  renameSync(tmpPath, path);
}

// --- In-process write locks ---

const locks = new Map<string, Promise<void>>();

async function withLock<T>(key: string, fn: () => T): Promise<T> {
  while (locks.has(key)) {
    await locks.get(key);
  }
  let resolveLock: () => void;
  const lockPromise = new Promise<void>((r) => { resolveLock = r; });
  locks.set(key, lockPromise);
  try {
    return fn();
  } finally {
    locks.delete(key);
    resolveLock!();
  }
}

// --- Path safety ---

function safePath(baseDir: string, id: string, ext: string): string {
  assertValidId(id);
  const filePath = join(baseDir, `${id}${ext}`);
  const resolved = resolve(filePath);
  const resolvedBase = resolve(baseDir);
  if (!resolved.startsWith(resolvedBase)) {
    throw new Error(`Path traversal detected: ${id}`);
  }
  return filePath;
}

// --- Catalog operations ---

export function readCatalogIndex(): CatalogIndex {
  return readJSON<CatalogIndex>(CATALOG_INDEX, {
    datasets: [],
    lastUpdated: new Date().toISOString(),
  });
}

export function writeCatalogIndex(index: CatalogIndex): void {
  index.lastUpdated = new Date().toISOString();
  writeJSON(CATALOG_INDEX, index);
}

export async function addDataset(entry: DatasetEntry, file: DatasetFile): Promise<void> {
  assertValidId(entry.id);
  return withLock("catalog", () => {
    ensureDir(DATASETS_DIR);
    const filePath = safePath(DATASETS_DIR, entry.id, ".json");
    writeJSON(filePath, file);

    const index = readCatalogIndex();
    const existing = index.datasets.findIndex((d) => d.id === entry.id);
    if (existing >= 0) {
      index.datasets[existing] = entry;
    } else {
      index.datasets.push(entry);
    }
    writeCatalogIndex(index);
  });
}

export function getDataset(id: string): DatasetFile | null {
  assertValidId(id);
  const filePath = safePath(DATASETS_DIR, id, ".json");
  if (!existsSync(filePath)) return null;
  return readJSON<DatasetFile>(filePath, null as unknown as DatasetFile);
}

export function listDatasets(): DatasetEntry[] {
  return readCatalogIndex().datasets;
}

// --- Viz operations ---

export function readVizIndex(): VizIndex {
  return readJSON<VizIndex>(VIZ_INDEX, {
    visualizations: [],
    lastUpdated: new Date().toISOString(),
  });
}

export function writeVizIndex(index: VizIndex): void {
  index.lastUpdated = new Date().toISOString();
  writeJSON(VIZ_INDEX, index);
}

export async function addVisualization(
  entry: VizEntry,
  htmlCode: string,
  notebookCode?: string,
): Promise<void> {
  assertValidId(entry.id);
  return withLock("viz", () => {
    ensureDir(VIZ_FILES_DIR);
    const filePath = safePath(VIZ_FILES_DIR, entry.id, ".html");
    writeFileSync(filePath, htmlCode, "utf-8");

    entry.codeFilePath = `viz/${entry.id}.html`;
    entry.generatedCode = htmlCode;

    if (notebookCode) {
      ensureDir(NOTEBOOKS_DIR);
      const nbPath = safePath(NOTEBOOKS_DIR, entry.id, ".py");
      writeFileSync(nbPath, notebookCode, "utf-8");
      entry.notebookPath = `notebooks/${entry.id}.py`;
    }

    const index = readVizIndex();
    const existing = index.visualizations.findIndex((v) => v.id === entry.id);
    if (existing >= 0) {
      index.visualizations[existing] = entry;
    } else {
      index.visualizations.push(entry);
    }
    writeVizIndex(index);
  });
}

export function getVisualization(id: string): VizEntry | null {
  assertValidId(id);
  const index = readVizIndex();
  return index.visualizations.find((v) => v.id === id) ?? null;
}

export function listVisualizations(): VizEntry[] {
  return readVizIndex().visualizations;
}

export function getVizHtml(id: string): string | null {
  assertValidId(id);
  const filePath = safePath(VIZ_FILES_DIR, id, ".html");
  if (!existsSync(filePath)) return null;
  try {
    return readFileSync(filePath, "utf-8");
  } catch (err) {
    console.error(`[catalog] Failed to read viz HTML for ${id}:`, err instanceof Error ? err.message : err);
    return null;
  }
}

export function getVizNotebook(id: string): string | null {
  assertValidId(id);
  const filePath = safePath(NOTEBOOKS_DIR, id, ".py");
  if (!existsSync(filePath)) return null;
  try {
    return readFileSync(filePath, "utf-8");
  } catch (err) {
    console.error(`[catalog] Failed to read notebook for ${id}:`, err instanceof Error ? err.message : err);
    return null;
  }
}

const WASM_DIR = join(NOTEBOOKS_DIR, "wasm");

export function getVizNotebookWasm(id: string): string | null {
  assertValidId(id);
  const filePath = safePath(WASM_DIR, id, ".html");
  if (!existsSync(filePath)) return null;
  try {
    return readFileSync(filePath, "utf-8");
  } catch (err) {
    console.error(`[catalog] Failed to read WASM notebook for ${id}:`, err instanceof Error ? err.message : err);
    return null;
  }
}

export async function addVizNotebook(id: string, code: string): Promise<void> {
  assertValidId(id);
  return withLock("viz", () => {
    ensureDir(NOTEBOOKS_DIR);
    const nbPath = safePath(NOTEBOOKS_DIR, id, ".py");
    writeFileSync(nbPath, code, "utf-8");

    const index = readVizIndex();
    const viz = index.visualizations.find((v) => v.id === id);
    if (viz) {
      viz.notebookPath = `notebooks/${id}.py`;
      writeVizIndex(index);
    }
  });
}

export function nextVizId(): string {
  const index = readVizIndex();
  let maxNum = 0;
  for (const v of index.visualizations) {
    const match = v.id.match(/^viz-(\d+)$/);
    if (match) {
      const num = parseInt(match[1], 10);
      if (num > maxNum) maxNum = num;
    }
  }
  return `viz-${String(maxNum + 1).padStart(3, "0")}`;
}
