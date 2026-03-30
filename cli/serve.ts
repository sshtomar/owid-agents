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
  const viz = getVisualization(req.params.id);
  const html = getVizHtml(req.params.id);
  if (!html || !viz) {
    res.status(404).send("Visualization not found");
    return;
  }

  const siteUrl = "https://ourworldbyagents.com";
  const chartUrl = `${siteUrl}/viz/${req.params.id}`;

  // Inject attribution footer before closing </body>
  const attribution = `
<div style="margin-top:16px;padding-top:10px;border-top:1px solid #E2E0D5;display:flex;justify-content:space-between;align-items:center;font-family:'Inter',sans-serif;font-size:10px;color:#7A786F;">
  <a href="${chartUrl}" target="_blank" rel="noopener" style="color:#EA5E33;text-decoration:none;font-weight:500;letter-spacing:0.2px;">
    ourworldbyagents.com
  </a>
  <a href="${chartUrl}" target="_blank" rel="noopener" style="color:#7A786F;text-decoration:none;">
    Explore this chart &#8599;
  </a>
</div>`;

  const embedHtml = html.replace("</body>", `${attribution}\n</body>`);

  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("X-Frame-Options", "ALLOWALL");
  res.setHeader("Content-Security-Policy", "frame-ancestors *");
  res.type("text/html").send(embedHtml);
});

// --- Share page (Open Graph meta tags for link previews on social/chat platforms) ---

app.get("/share/:id", validateId, (req, res) => {
  const viz = getVisualization(req.params.id);
  if (!viz) {
    res.status(404).send("Visualization not found");
    return;
  }

  const siteUrl = "https://ourworldbyagents.com";
  const chartUrl = `${siteUrl}/viz/${req.params.id}`;
  const embedUrl = `${siteUrl}/embed/${req.params.id}`;
  const oembedUrl = `${siteUrl}/api/oembed?url=${encodeURIComponent(chartUrl)}&format=json`;
  const description = viz.description.slice(0, 200);

  // Serve a minimal HTML page with OG tags that redirects to the SPA
  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>${viz.title} - Our World by Agents</title>
  <meta property="og:title" content="${viz.title}">
  <meta property="og:description" content="${description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="${chartUrl}">
  <meta property="og:site_name" content="Our World by Agents">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${viz.title}">
  <meta name="twitter:description" content="${description}">
  <link rel="alternate" type="application/json+oembed" href="${oembedUrl}" title="${viz.title}">
  <meta http-equiv="refresh" content="0;url=${chartUrl}">
</head>
<body>
  <p>Redirecting to <a href="${chartUrl}">${viz.title}</a>...</p>
</body>
</html>`;

  res.type("text/html").send(html);
});

// --- oEmbed endpoint (enables auto-embed in WordPress, Medium, Notion, etc.) ---

app.get("/api/oembed", (req, res) => {
  const url = req.query.url as string | undefined;
  if (!url) {
    res.status(400).json({ error: "url parameter required" });
    return;
  }

  const match = url.match(/\/viz\/(viz-\d+)/);
  if (!match || !isValidId(match[1])) {
    res.status(404).json({ error: "No matching visualization" });
    return;
  }

  const vizId = match[1];
  const viz = getVisualization(vizId);
  if (!viz) {
    res.status(404).json({ error: "Visualization not found" });
    return;
  }

  const siteUrl = "https://ourworldbyagents.com";
  const width = parseInt(req.query.maxwidth as string) || 800;
  const height = parseInt(req.query.maxheight as string) || 600;

  res.json({
    version: "1.0",
    type: "rich",
    provider_name: "Our World by Agents",
    provider_url: siteUrl,
    title: viz.title,
    description: viz.description,
    width,
    height,
    html: `<iframe src="${siteUrl}/embed/${vizId}" width="${width}" height="${height}" loading="lazy" style="border:0" allow="web-share"></iframe>`,
    thumbnail_url: undefined,
  });
});

// --- Electricity Map endpoint ---

interface CountryElectricity {
  countryName: string;
  countryCode: string;
  carbonIntensity: number | null;
  shareClean: number | null;
  shareFossil: number | null;
  shareRenewables: number | null;
  demandTotal: number | null;
  demandPerCapita: number | null;
  emissionsTotal: number | null;
  generationTotal: number | null;
  generationMix: {
    coal: number | null;
    gas: number | null;
    nuclear: number | null;
    hydro: number | null;
    wind: number | null;
    solar: number | null;
    bioenergy: number | null;
  };
}

interface MetricInfo {
  key: string;
  label: string;
  unit: string;
}

const ELECTRICITY_METRICS: MetricInfo[] = [
  { key: "carbonIntensity", label: "Carbon Intensity", unit: "gCO2/kWh" },
  { key: "shareClean", label: "Clean Share", unit: "%" },
  { key: "shareFossil", label: "Fossil Share", unit: "%" },
  { key: "shareRenewables", label: "Renewables Share", unit: "%" },
  { key: "demandPerCapita", label: "Demand per Capita", unit: "MWh" },
  { key: "demandTotal", label: "Total Demand", unit: "TWh" },
  { key: "emissionsTotal", label: "Total Emissions", unit: "mtCO2" },
  { key: "generationTotal", label: "Total Generation", unit: "TWh" },
];

const ELECTRICITY_DATASET_MAP: Record<string, string> = {
  carbonIntensity: "ember--EMISSIONS-INTENSITY",
  shareClean: "ember--SHARE-CLEAN",
  shareFossil: "ember--SHARE-FOSSIL",
  shareRenewables: "ember--SHARE-RENEWABLES",
  demandTotal: "ember--DEMAND-TOTAL",
  demandPerCapita: "ember--DEMAND-PER-CAPITA",
  emissionsTotal: "ember--EMISSIONS-TOTAL",
  generationTotal: "ember--GEN-TOTAL",
  generationClean: "ember--GEN-CLEAN",
  generationFossil: "ember--GEN-FOSSIL",
  generationWindSolar: "ember--GEN-WIND-SOLAR",
  shareCoal: "ember--SHARE-COAL",
  shareSolar: "ember--SHARE-SOLAR",
  shareWind: "ember--SHARE-WIND",
};

interface DataPoint {
  country: string;
  countryName: string;
  year: number;
  value: number | null;
}

// Cached aggregation
let electricityCache: {
  availableYears: number[];
  availableMetrics: MetricInfo[];
  data: Record<number, Record<string, CountryElectricity>>;
} | null = null;

function buildElectricityData() {
  if (electricityCache) return electricityCache;

  // Load all datasets and index by (year, country)
  const dataByField = new Map<string, Map<string, Map<number, number>>>();

  for (const [field, datasetId] of Object.entries(ELECTRICITY_DATASET_MAP)) {
    const dataset = getDataset(datasetId);
    if (!dataset) continue;

    const byCountryYear = new Map<string, Map<number, number>>();
    for (const dp of dataset.data as DataPoint[]) {
      if (dp.value === null) continue;
      let yearMap = byCountryYear.get(dp.country);
      if (!yearMap) {
        yearMap = new Map();
        byCountryYear.set(dp.country, yearMap);
      }
      yearMap.set(dp.year, dp.value);
    }
    dataByField.set(field, byCountryYear);
  }

  // Collect all years and country names
  const allYears = new Set<number>();
  const countryNames = new Map<string, string>();

  for (const [field, datasetId] of Object.entries(ELECTRICITY_DATASET_MAP)) {
    const dataset = getDataset(datasetId);
    if (!dataset) continue;
    for (const dp of dataset.data as DataPoint[]) {
      allYears.add(dp.year);
      if (!countryNames.has(dp.country)) {
        countryNames.set(dp.country, dp.countryName);
      }
    }
  }

  const years = Array.from(allYears).sort((a, b) => a - b);
  const allCountries = Array.from(countryNames.keys());

  function getValue(field: string, country: string, year: number): number | null {
    return dataByField.get(field)?.get(country)?.get(year) ?? null;
  }

  const data: Record<number, Record<string, CountryElectricity>> = {};

  for (const year of years) {
    const yearData: Record<string, CountryElectricity> = {};
    for (const code of allCountries) {
      const total = getValue("generationTotal", code, year);
      const sCoal = getValue("shareCoal", code, year);
      const sSolar = getValue("shareSolar", code, year);
      const sWind = getValue("shareWind", code, year);
      const sClean = getValue("shareClean", code, year);
      const sFossil = getValue("shareFossil", code, year);
      const sRenew = getValue("shareRenewables", code, year);

      // Compute generation mix from shares * total
      // Clean = nuclear + hydro + wind + solar + bioenergy
      // Fossil = coal + gas + other fossil
      const genClean = getValue("generationClean", code, year);
      const genFossil = getValue("generationFossil", code, year);
      const genWindSolar = getValue("generationWindSolar", code, year);

      // Estimate individual fuels from shares and total generation
      const coalTWh = total !== null && sCoal !== null ? total * sCoal / 100 : null;
      const solarTWh = total !== null && sSolar !== null ? total * sSolar / 100 : null;
      const windTWh = total !== null && sWind !== null ? total * sWind / 100 : null;

      // Gas = fossil - coal (rough estimate)
      const gasTWh = genFossil !== null && coalTWh !== null
        ? Math.max(0, genFossil - coalTWh)
        : null;

      // Nuclear = clean - renewables (if we have both)
      const renewTWh = total !== null && sRenew !== null ? total * sRenew / 100 : null;
      const nuclearTWh = genClean !== null && renewTWh !== null
        ? Math.max(0, genClean - renewTWh)
        : null;

      // Hydro = renewables - wind - solar - bioenergy (estimate bio as small remainder)
      const hydroTWh = renewTWh !== null && windTWh !== null && solarTWh !== null
        ? Math.max(0, renewTWh - windTWh - solarTWh)
        : null;

      yearData[code] = {
        countryName: countryNames.get(code) ?? code,
        countryCode: code,
        carbonIntensity: getValue("carbonIntensity", code, year),
        shareClean: sClean,
        shareFossil: sFossil,
        shareRenewables: sRenew,
        demandTotal: getValue("demandTotal", code, year),
        demandPerCapita: getValue("demandPerCapita", code, year),
        emissionsTotal: getValue("emissionsTotal", code, year),
        generationTotal: total,
        generationMix: {
          coal: coalTWh,
          gas: gasTWh,
          nuclear: nuclearTWh,
          hydro: hydroTWh,
          wind: windTWh,
          solar: solarTWh,
          bioenergy: null,
        },
      };
    }
    data[year] = yearData;
  }

  electricityCache = {
    availableYears: years,
    availableMetrics: ELECTRICITY_METRICS,
    data,
  };

  return electricityCache;
}

app.get("/api/electricity-map", (_req, res) => {
  try {
    const result = buildElectricityData();
    res.json(result);
  } catch (err) {
    console.error("[api] Failed to build electricity map data:", err instanceof Error ? err.message : err);
    res.status(500).json({ error: "Failed to build electricity map data" });
  }
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
