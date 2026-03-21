export interface VizEntry {
  id: string;
  title: string;
  description: string;
  chartType: string;
  highlights: string[];
  createdAt: string;
  generatedCode: string;
  notebookPath?: string;
}

export interface VizListResponse {
  visualizations: VizEntry[];
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

export function vizSearchable(viz: VizEntry): string {
  return [viz.title, viz.description, viz.chartType, ...viz.highlights]
    .join(" ")
    .toLowerCase();
}

export function matchesSearch(viz: VizEntry, query: string): boolean {
  return vizSearchable(viz).includes(query.toLowerCase());
}

export function matchesTheme(viz: VizEntry, theme: Theme): boolean {
  const text = vizSearchable(viz);
  return theme.keywords.some((kw) => text.includes(kw));
}
