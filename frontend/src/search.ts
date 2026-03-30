import Fuse from "fuse.js";

// Metadata-only viz entry (no generatedCode from the list endpoint)
export interface VizMeta {
  id: string;
  title: string;
  description: string;
  chartType: string;
  highlights: string[];
  createdAt: string;
  datasetIds: string[];
  codeFilePath: string;
  notebookPath?: string;
}

export interface VizListResponse {
  visualizations: VizMeta[];
  count: number;
}

export interface Theme {
  label: string;
  keywords: string[];
}

export const THEMES: Theme[] = [
  {
    label: "Health",
    keywords: [
      "life expectancy", "mortality", "malaria", "vaccine", "immunization",
      "health spending", "tuberculosis", "suicide", "non-communicable",
      "obesity", "stunting", "skilled health", "births attended", "road traffic",
      "tobacco", "smoking", "saved children", "ncd", "cancer", "diabetes",
      "cardiovascular", "air pollution", "pm2.5",
    ],
  },
  {
    label: "Economy",
    keywords: [
      "gdp", "wealth", "income", "debt", "inflation", "poverty", "gini",
      "inequality", "fiscal", "current account", "trade", "household debt",
      "remittance", "economic", "consumer prices", "lending", "borrowing",
    ],
  },
  {
    label: "Environment",
    keywords: [
      "co2", "carbon", "emission", "renewable", "forest", "water stress",
      "freshwater", "natural disaster", "climate", "greenhouse", "ghg",
      "clean fuel", "cooking", "deforestation", "catastrophe",
    ],
  },
  {
    label: "Conflict",
    keywords: [
      "refugee", "displaced", "homicide", "military", "violence", "war",
      "forced from home", "guns and butter", "safety divide", "idp",
    ],
  },
  {
    label: "Education",
    keywords: [
      "education", "school", "enrollment", "tertiary", "university",
      "out-of-school", "investing in minds", "university boom",
    ],
  },
  {
    label: "Gender",
    keywords: [
      "women", "female", "gender pay gap", "parliament", "labor force participation",
      "half the sky",
    ],
  },
  {
    label: "Energy",
    keywords: [
      "electricity", "nuclear", "renewable energy", "energy consumption",
      "lighting up", "atomic", "clean fuel", "power generation",
    ],
  },
  {
    label: "Governance",
    keywords: [
      "democracy", "electoral", "government", "fiscal balance", "scorecard",
      "development", "happiness", "cantril",
    ],
  },
];

export function vizSearchable(viz: VizMeta): string {
  return [viz.title, viz.description, viz.chartType, ...viz.highlights]
    .join(" ")
    .toLowerCase();
}

// Fuzzy search using Fuse.js
export function createFuseIndex(vizList: VizMeta[]): Fuse<VizMeta> {
  return new Fuse(vizList, {
    keys: [
      { name: "title", weight: 3 },
      { name: "description", weight: 2 },
      { name: "chartType", weight: 1 },
      { name: "highlights", weight: 1.5 },
    ],
    threshold: 0.35,
    ignoreLocation: true,
    includeScore: true,
  });
}

export function fuzzySearch(fuse: Fuse<VizMeta>, query: string): VizMeta[] {
  if (!query.trim()) return [];
  return fuse.search(query).map((result) => result.item);
}

export function matchesTheme(viz: VizMeta, theme: Theme): boolean {
  const text = vizSearchable(viz);
  return theme.keywords.some((kw) => text.includes(kw));
}

// Find related charts by shared datasets or keyword overlap
export function findRelated(target: VizMeta, allViz: VizMeta[], limit = 3): VizMeta[] {
  const targetText = vizSearchable(target);
  const targetWords = new Set(targetText.split(/\s+/).filter((w) => w.length > 3));

  const scored = allViz
    .filter((v) => v.id !== target.id)
    .map((v) => {
      let score = 0;
      // Shared datasets
      const sharedDatasets = v.datasetIds.filter((d) => target.datasetIds.includes(d));
      score += sharedDatasets.length * 10;
      // Shared keywords
      const vText = vizSearchable(v);
      const vWords = new Set(vText.split(/\s+/).filter((w) => w.length > 3));
      for (const word of targetWords) {
        if (vWords.has(word)) score += 1;
      }
      return { viz: v, score };
    })
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score);

  return scored.slice(0, limit).map((s) => s.viz);
}
