import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://api.ourworldindata.org/v1/indicators";

// Curated catalog of interesting OWID indicators with their numeric IDs
const INDICATORS: Record<
  string,
  {
    name: string;
    description: string;
    topics: string[];
    sourceNote: string;
  }
> = {
  "1210090": {
    name: "Happiness Score (Cantril Ladder, 0-10)",
    description:
      "Self-reported life satisfaction on a 0-10 scale from the Gallup World Poll",
    topics: ["happiness", "wellbeing"],
    sourceNote: "World Happiness Report / Gallup World Poll",
  },
  "1209753": {
    name: "Electoral Democracy Index (0-1)",
    description:
      "V-Dem Electoral Democracy Index measuring the quality of elections, freedoms, and institutional constraints",
    topics: ["democracy", "governance", "politics"],
    sourceNote: "V-Dem (Varieties of Democracy)",
  },
  "899981": {
    name: "Deaths from Natural Disasters",
    description:
      "Total number of deaths from all natural disaster types including earthquakes, floods, storms, droughts",
    topics: ["disasters", "climate", "mortality"],
    sourceNote: "EM-DAT International Disaster Database",
  },
  "1134914": {
    name: "Nuclear Share of Electricity (%)",
    description:
      "Share of electricity generated from nuclear power plants",
    topics: ["energy", "nuclear"],
    sourceNote: "Ember / Energy Institute",
  },
  "899970": {
    name: "Economic Damages from Natural Disasters (US$)",
    description:
      "Total economic damages from all natural disaster types in current US dollars",
    topics: ["disasters", "economics"],
    sourceNote: "EM-DAT International Disaster Database",
  },
  "1210053": {
    name: "Political Regime Type",
    description:
      "Classification of political regime: closed autocracy (0), electoral autocracy (1), electoral democracy (2), liberal democracy (3)",
    topics: ["democracy", "governance", "politics"],
    sourceNote: "V-Dem / Regimes of the World",
  },
};

interface OWIDDataResponse {
  values: number[];
  years: number[];
  entities: number[];
}

interface OWIDMetadataResponse {
  dimensions: {
    entities: {
      values: Array<{ id: number; name: string; code: string }>;
    };
  };
  display?: { name?: string };
  name?: string;
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`OWID API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  return Object.entries(INDICATORS)
    .filter(
      ([, v]) =>
        v.name.toLowerCase().includes(q) ||
        v.description.toLowerCase().includes(q) ||
        v.topics.some((t) => t.includes(q)) ||
        v.sourceNote.toLowerCase().includes(q)
    )
    .slice(0, limit)
    .map(([id, v]) => ({
      id,
      name: v.name,
      description: `${v.description} [${v.sourceNote}]`,
      source: "Our World in Data",
      topics: v.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];

  // Fetch data and metadata in parallel
  const [dataResponse, metaResponse] = await Promise.all([
    fetchJSON<OWIDDataResponse>(`${BASE}/${indicatorId}.data.json`),
    fetchJSON<OWIDMetadataResponse>(`${BASE}/${indicatorId}.metadata.json`),
  ]);

  const name =
    indicator?.name ??
    metaResponse.display?.name ??
    metaResponse.name ??
    `Indicator ${indicatorId}`;

  // Build entity ID -> {name, code} lookup
  const entityMap = new Map<number, { name: string; code: string }>();
  for (const entity of metaResponse.dimensions.entities.values) {
    entityMap.set(entity.id, { name: entity.name, code: entity.code ?? "" });
  }

  // Filter countries if specified
  const countryFilter = countries
    ? new Set(countries.split(",").map((c) => c.trim().toUpperCase()))
    : null;

  const data: DataPoint[] = [];
  for (let i = 0; i < dataResponse.values.length; i++) {
    const entityId = dataResponse.entities[i];
    const entity = entityMap.get(entityId);
    if (!entity || !entity.code) continue;

    // Skip aggregates (entities without ISO codes or with long codes)
    if (entity.code.length > 3) continue;

    if (countryFilter && !countryFilter.has(entity.code)) continue;

    const value = dataResponse.values[i];
    if (value === null || value === undefined) continue;

    data.push({
      country: entity.code,
      countryName: entity.name,
      year: dataResponse.years[i],
      value,
    });
  }

  data.sort((a, b) => a.year - b.year);

  // Trim to 10000 points if needed
  const trimmed = data.length > 10000 ? data.slice(-10000) : data;

  return { name, data: trimmed };
}

export function getSourceUrl(indicatorId: string): string {
  return `https://ourworldindata.org`;
}
