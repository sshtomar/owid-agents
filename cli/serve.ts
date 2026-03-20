import express from "express";
import cors from "cors";
import {
  listDatasets,
  getDataset,
  listVisualizations,
  getVisualization,
  getVizHtml,
} from "../src/catalog.js";

const app = express();
const PORT = parseInt(process.env.PORT ?? "3001", 10);

app.use(cors());
app.use(express.json());

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

// --- Health ---

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok" });
});

app.listen(PORT, () => {
  console.log(`API server running at http://localhost:${PORT}`);
});
