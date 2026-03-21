import express from "express";
import cors from "cors";
import { join } from "node:path";
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

// --- Health ---

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

if (!process.env.VERCEL) {
  app.listen(PORT, () => {
    console.log(`API server running at http://localhost:${PORT}`);
  });
}
