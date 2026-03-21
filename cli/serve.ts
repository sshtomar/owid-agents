import express from "express";
import cors from "cors";
import { join } from "node:path";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { randomUUID } from "node:crypto";
import {
  listDatasets,
  getDataset,
  listVisualizations,
  getVisualization,
  getVizHtml,
  getVizNotebook,
  getVizNotebookWasm,
} from "../src/catalog.js";

export const app = express();
const PORT = parseInt(process.env.PORT ?? "3001", 10);

const WASM_NOTEBOOKS_DIR = join(
  import.meta.dirname,
  "..",
  "data",
  "visualizations",
  "notebooks",
  "wasm",
);

app.use(cors());
app.use(express.json());
app.use("/wasm-notebooks", express.static(WASM_NOTEBOOKS_DIR));

// --- Dataset endpoints ---

app.get("/api/datasets", (_req, res) => {
  const datasets = listDatasets();
  res.json({ datasets, count: datasets.length });
});

app.get("/api/datasets/:id", (req, res) => {
  const dataset = getDataset(req.params.id);
  if (!dataset) {
    res.status(404).json({ error: "Dataset not found" });
    return;
  }
  res.json(dataset);
});

// --- Visualization endpoints ---

app.get("/api/visualizations", (_req, res) => {
  const visualizations = listVisualizations().map((v) => {
    if (!v.generatedCode) {
      const html = getVizHtml(v.id);
      if (html) v.generatedCode = html;
    }
    return v;
  });
  res.json({ visualizations, count: visualizations.length });
});

app.get("/api/visualizations/:id", (req, res) => {
  const viz = getVisualization(req.params.id);
  if (!viz) {
    res.status(404).json({ error: "Visualization not found" });
    return;
  }
  const html = getVizHtml(req.params.id);
  res.json({ ...viz, htmlCode: html });
});

app.get("/api/visualizations/:id/notebook/wasm", (req, res) => {
  const viz = getVisualization(req.params.id);
  if (!viz?.notebookPath || !getVizNotebookWasm(req.params.id)) {
    res.status(404).json({ error: "WASM notebook not found" });
    return;
  }
  res.redirect(`/wasm-notebooks/${req.params.id}.html`);
});

app.get("/api/visualizations/:id/notebook", (req, res) => {
  const notebook = getVizNotebook(req.params.id);
  if (!notebook) {
    res.status(404).json({ error: "Notebook not found" });
    return;
  }
  res.type("text/plain").send(notebook);
});

// --- Feedback & Requests storage helpers ---

const DATA_DIR = join(import.meta.dirname, "..", "data");
const FEEDBACK_PATH = join(DATA_DIR, "feedback.json");
const REQUESTS_PATH = join(DATA_DIR, "requests.json");

type Reaction = "useful" | "interesting" | "surprising" | "needs-work";
const VALID_REACTIONS: Reaction[] = ["useful", "interesting", "surprising", "needs-work"];

interface FeedbackEntry {
  id: string;
  vizId: string;
  reaction: Reaction;
  comment?: string;
  createdAt: string;
}

interface RequestEntry {
  id: string;
  topic: string;
  description?: string;
  name?: string;
  createdAt: string;
}

function readJsonArray<T>(path: string): T[] {
  if (!existsSync(path)) return [];
  return JSON.parse(readFileSync(path, "utf-8")) as T[];
}

function appendJson<T>(path: string, entry: T): void {
  const arr = readJsonArray<T>(path);
  arr.push(entry);
  writeFileSync(path, JSON.stringify(arr, null, 2));
}

// --- Feedback endpoints ---

app.post("/api/feedback", (req, res) => {
  const { vizId, reaction, comment } = req.body;
  if (!vizId || !reaction || !VALID_REACTIONS.includes(reaction)) {
    res.status(400).json({ error: "vizId and valid reaction required" });
    return;
  }
  const entry: FeedbackEntry = {
    id: randomUUID(),
    vizId,
    reaction,
    comment: comment || undefined,
    createdAt: new Date().toISOString(),
  };
  appendJson(FEEDBACK_PATH, entry);
  res.json(entry);
});

app.get("/api/feedback/:vizId", (req, res) => {
  const all = readJsonArray<FeedbackEntry>(FEEDBACK_PATH);
  const feedback = all.filter((f) => f.vizId === req.params.vizId);
  const counts: Record<Reaction, number> = {
    useful: 0,
    interesting: 0,
    surprising: 0,
    "needs-work": 0,
  };
  for (const f of feedback) {
    counts[f.reaction]++;
  }
  res.json({ feedback, counts });
});

// --- Dataset request endpoints ---

app.post("/api/requests", (req, res) => {
  const { topic, description, name } = req.body;
  if (!topic) {
    res.status(400).json({ error: "topic is required" });
    return;
  }
  const entry: RequestEntry = {
    id: randomUUID(),
    topic,
    description: description || undefined,
    name: name || undefined,
    createdAt: new Date().toISOString(),
  };
  appendJson(REQUESTS_PATH, entry);
  res.json(entry);
});

app.get("/api/requests", (_req, res) => {
  const requests = readJsonArray<RequestEntry>(REQUESTS_PATH);
  res.json({ requests });
});

// --- Health ---

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

if (!process.env.VERCEL) {
  app.listen(PORT, () => {
    console.log(`API server running at http://localhost:${PORT}`);
  });
}
