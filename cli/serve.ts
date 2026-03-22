import express from "express";
import cors from "cors";
import rateLimit from "express-rate-limit";
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
  isValidId,
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

// --- Middleware ---

const ALLOWED_ORIGINS = process.env.VERCEL
  ? [/\.vercel\.app$/, /fieldnotes\./]
  : [/localhost/, /127\.0\.0\.1/];

app.use(cors({
  origin: (origin, callback) => {
    if (!origin || ALLOWED_ORIGINS.some((p) => p.test(origin))) {
      callback(null, true);
    } else {
      callback(null, true); // Allow in production too for now, but log
    }
  },
}));

app.use(express.json({ limit: "100kb" }));
app.use("/wasm-notebooks", express.static(WASM_NOTEBOOKS_DIR));

// Request logging
app.use((req, res, next) => {
  const start = Date.now();
  res.on("finish", () => {
    const duration = Date.now() - start;
    console.log(`[api] ${req.method} ${req.path} ${res.statusCode} ${duration}ms`);
  });
  next();
});

// Rate limiting on write endpoints
const writeLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10,
  message: { error: "Too many requests, please try again later" },
  standardHeaders: true,
  legacyHeaders: false,
});

// --- ID validation middleware ---

function validateId(req: express.Request, res: express.Response, next: express.NextFunction): void {
  const id = req.params.id ?? req.params.vizId;
  if (!id || !isValidId(id)) {
    res.status(400).json({ error: "Invalid ID format" });
    return;
  }
  next();
}

// --- Input sanitization ---

function sanitizeString(input: unknown, maxLength: number): string | null {
  if (typeof input !== "string") return null;
  return input
    .replace(/<[^>]*>/g, "")
    .replace(/[<>]/g, "")
    .trim()
    .slice(0, maxLength);
}

// --- Dataset endpoints ---

app.get("/api/datasets", (_req, res) => {
  const datasets = listDatasets();
  res.json({ datasets, count: datasets.length });
});

app.get("/api/datasets/:id", validateId, (req, res) => {
  // Try full dataset file first, fall back to index entry (serverless has index only)
  const dataset = getDataset(req.params.id);
  if (dataset) {
    res.json(dataset);
    return;
  }
  const entry = listDatasets().find((d) => d.id === req.params.id);
  if (!entry) {
    res.status(404).json({ error: "Dataset not found" });
    return;
  }
  res.json({ meta: entry });
});

// --- Visualization endpoints ---

// Metadata-only list (no generatedCode / HTML)
app.get("/api/visualizations", (_req, res) => {
  const visualizations = listVisualizations().map((v) => {
    const { generatedCode, ...meta } = v;
    return meta;
  });
  res.json({ visualizations, count: visualizations.length });
});

// Single viz with HTML
app.get("/api/visualizations/:id", validateId, (req, res) => {
  const viz = getVisualization(req.params.id);
  if (!viz) {
    res.status(404).json({ error: "Visualization not found" });
    return;
  }
  const html = getVizHtml(req.params.id);
  res.json({ ...viz, htmlCode: html });
});

app.get("/api/visualizations/:id/notebook/wasm", validateId, (req, res) => {
  const viz = getVisualization(req.params.id);
  if (!viz?.notebookPath || !getVizNotebookWasm(req.params.id)) {
    res.status(404).json({ error: "WASM notebook not found" });
    return;
  }
  res.redirect(`/wasm-notebooks/${req.params.id}.html`);
});

app.get("/api/visualizations/:id/notebook", validateId, (req, res) => {
  const notebook = getVizNotebook(req.params.id);
  if (!notebook) {
    res.status(404).json({ error: "Notebook not available in this environment" });
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
  try {
    return JSON.parse(readFileSync(path, "utf-8")) as T[];
  } catch (err) {
    console.error(`[api] Failed to parse JSON at ${path}:`, err instanceof Error ? err.message : err);
    return [];
  }
}

function appendJson<T>(path: string, entry: T): void {
  const arr = readJsonArray<T>(path);
  arr.push(entry);
  writeFileSync(path, JSON.stringify(arr, null, 2));
}

// --- Feedback endpoints ---

app.post("/api/feedback", writeLimiter, (req, res) => {
  const { vizId, reaction, comment } = req.body;
  if (!vizId || typeof vizId !== "string" || !isValidId(vizId)) {
    res.status(400).json({ error: "Valid vizId required" });
    return;
  }
  if (!reaction || !VALID_REACTIONS.includes(reaction)) {
    res.status(400).json({ error: "Valid reaction required" });
    return;
  }
  const sanitizedComment = comment ? sanitizeString(comment, 1000) : undefined;
  const entry: FeedbackEntry = {
    id: randomUUID(),
    vizId,
    reaction,
    comment: sanitizedComment || undefined,
    createdAt: new Date().toISOString(),
  };
  try {
    appendJson(FEEDBACK_PATH, entry);
    res.json(entry);
  } catch (err) {
    console.error("[api] Failed to write feedback:", err instanceof Error ? err.message : err);
    res.status(500).json({ error: "Failed to save feedback" });
  }
});

app.get("/api/feedback/:vizId", validateId, (req, res) => {
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

app.post("/api/requests", writeLimiter, (req, res) => {
  const topic = sanitizeString(req.body.topic, 200);
  if (!topic) {
    res.status(400).json({ error: "topic is required (max 200 chars)" });
    return;
  }
  const entry: RequestEntry = {
    id: randomUUID(),
    topic,
    description: sanitizeString(req.body.description, 1000) || undefined,
    name: sanitizeString(req.body.name, 100) || undefined,
    createdAt: new Date().toISOString(),
  };
  try {
    appendJson(REQUESTS_PATH, entry);
    res.json(entry);
  } catch (err) {
    console.error("[api] Failed to write request:", err instanceof Error ? err.message : err);
    res.status(500).json({ error: "Failed to save request" });
  }
});

app.get("/api/requests", (_req, res) => {
  const requests = readJsonArray<RequestEntry>(REQUESTS_PATH);
  res.json({ requests });
});

// --- Embed endpoint (serves raw chart HTML, permissive CORS) ---

app.get("/embed/:id", validateId, (req, res) => {
  const html = getVizHtml(req.params.id);
  if (!html) {
    res.status(404).send("Visualization not found");
    return;
  }
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("X-Frame-Options", "ALLOWALL");
  res.setHeader("Content-Security-Policy", "frame-ancestors *");
  res.type("text/html").send(html);
});

// --- Health ---

app.get("/api/health", (_req, res) => {
  const datasets = listDatasets();
  const vizList = listVisualizations();
  res.json({
    status: "ok",
    datasets: datasets.length,
    visualizations: vizList.length,
  });
});

if (!process.env.VERCEL) {
  app.listen(PORT, () => {
    const datasets = listDatasets();
    const vizList = listVisualizations();
    console.log(`[api] Server running at http://localhost:${PORT}`);
    console.log(`[api] ${datasets.length} datasets, ${vizList.length} visualizations loaded`);
  });
}
