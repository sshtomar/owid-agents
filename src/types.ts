export type Provider =
  | "world-bank"
  | "who-gho"
  | "un-sdg"
  | "eurostat"
  | "unhcr"
  | "imf"
  | "owid"
  | "unesco";

export interface DataPoint {
  country: string;
  countryName: string;
  year: number;
  value: number | null;
}

export interface DatasetEntry {
  id: string;
  title: string;
  description: string;
  source: {
    provider: Provider;
    indicatorId: string;
    indicatorName: string;
    sourceUrl: string;
    lastFetched: string;
  };
  topics: string[];
  countries: string[];
  dateRange: { start: string; end: string };
  dataPointCount: number;
  dataFilePath: string;
}

export interface DatasetFile {
  meta: DatasetEntry;
  data: DataPoint[];
}

export interface VizEntry {
  id: string;
  title: string;
  description: string;
  datasetIds: string[];
  chartType: string;
  codeFilePath: string;
  generatedCode: string;
  highlights: string[];
  createdAt: string;
  notebookPath?: string;
}

export interface CatalogIndex {
  datasets: DatasetEntry[];
  lastUpdated: string;
}

export interface VizIndex {
  visualizations: VizEntry[];
  lastUpdated: string;
}

export interface IndicatorSearchResult {
  id: string;
  name: string;
  description: string;
  source: string;
  topics: string[];
}
