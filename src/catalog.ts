import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import type {
  CatalogIndex,
  VizIndex,
  DatasetEntry,
  DatasetFile,
  VizEntry,
} from "./types.js";

const DATA_DIR = join(import.meta.dirname, "..", "data");
const CATALOG_DIR = join(DATA_DIR, "catalog");
const DATASETS_DIR = join(CATALOG_DIR, "datasets");
const VIZ_DIR = join(DATA_DIR, "visualizations");
const VIZ_FILES_DIR = join(VIZ_DIR, "viz");

const CATALOG_INDEX = join(CATALOG_DIR, "index.json");
const VIZ_INDEX = join(VIZ_DIR, "index.json");

function ensureDir(dir: string): void {
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

function readJSON<T>(path: string, fallback: T): T {
  if (!existsSync(path)) return fallback;
  const raw = readFileSync(path, "utf-8");
  return JSON.parse(raw) as T;
}

function writeJSON(path: string, data: unknown): void {
  ensureDir(dirname(path));
  writeFileSync(path, JSON.stringify(data, null, 2) + "\n", "utf-8");
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

export function addDataset(entry: DatasetEntry, file: DatasetFile): void {
  ensureDir(DATASETS_DIR);
  const filePath = join(DATASETS_DIR, `${entry.id}.json`);
  writeJSON(filePath, file);

  const index = readCatalogIndex();
  const existing = index.datasets.findIndex((d) => d.id === entry.id);
  if (existing >= 0) {
    index.datasets[existing] = entry;
  } else {
    index.datasets.push(entry);
  }
  writeCatalogIndex(index);
}

export function getDataset(id: string): DatasetFile | null {
  const filePath = join(DATASETS_DIR, `${id}.json`);
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

export function addVisualization(entry: VizEntry, htmlCode: string): void {
  ensureDir(VIZ_FILES_DIR);
  const filePath = join(VIZ_FILES_DIR, `${entry.id}.html`);
  writeFileSync(filePath, htmlCode, "utf-8");

  entry.codeFilePath = `viz/${entry.id}.html`;
  entry.generatedCode = htmlCode;

  const index = readVizIndex();
  const existing = index.visualizations.findIndex((v) => v.id === entry.id);
  if (existing >= 0) {
    index.visualizations[existing] = entry;
  } else {
    index.visualizations.push(entry);
  }
  writeVizIndex(index);
}

export function getVisualization(id: string): VizEntry | null {
  const index = readVizIndex();
  return index.visualizations.find((v) => v.id === id) ?? null;
}

export function listVisualizations(): VizEntry[] {
  return readVizIndex().visualizations;
}

export function getVizHtml(id: string): string | null {
  const filePath = join(VIZ_FILES_DIR, `${id}.html`);
  if (!existsSync(filePath)) return null;
  return readFileSync(filePath, "utf-8");
}

export function nextVizId(): string {
  const index = readVizIndex();
  const num = index.visualizations.length + 1;
  return `viz-${String(num).padStart(3, "0")}`;
}
