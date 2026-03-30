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
  "899531": {
    name: "Human Development Index",
    description:
      "Composite index measuring average achievement in health, education, and standard of living (0-1 scale)",
    topics: ["development", "health", "education", "living standards"],
    sourceNote: "UNDP Human Development Report",
  },
  "899527": {
    name: "Gender Inequality Index",
    description:
      "Composite measure of gender inequality using reproductive health, empowerment, and labor market dimensions (0-1, higher = more inequality)",
    topics: ["gender", "inequality", "development", "women"],
    sourceNote: "UNDP Human Development Report",
  },
  "1134904": {
    name: "Fossil Fuels Share of Electricity (%)",
    description:
      "Percentage of total electricity generation that comes from fossil fuels (coal, oil, gas)",
    topics: ["energy", "fossil fuels", "electricity", "climate"],
    sourceNote: "Ember / Energy Institute",
  },
  "899545": {
    name: "Material Footprint per Capita (tonnes)",
    description:
      "Total amount of raw materials extracted to meet consumption demands, measured in tonnes per person",
    topics: ["environment", "consumption", "resources", "sustainability"],
    sourceNote: "UN Environment Programme",
  },
  "1209730": {
    name: "Political Corruption Index (0-1)",
    description:
      "Measures the pervasiveness of political corruption including executive, legislative, and judicial corruption (0 = low, 1 = high)",
    topics: ["corruption", "governance", "politics", "institutions"],
    sourceNote: "V-Dem (Varieties of Democracy)",
  },
  "899535": {
    name: "Inequality-Adjusted Human Development Index",
    description:
      "HDI adjusted for inequalities in health, education, and income distribution within countries",
    topics: ["development", "inequality", "health", "education"],
    sourceNote: "UNDP Human Development Report",
  },
  "1134941": {
    name: "Solar and Wind Share of Electricity (%)",
    description:
      "Percentage of total electricity generation from solar and wind combined",
    topics: ["energy", "solar", "wind", "renewable energy", "climate"],
    sourceNote: "Ember / Energy Institute",
  },
  "1134943": {
    name: "Solar Share of Electricity (%)",
    description:
      "Percentage of total electricity generation from solar power",
    topics: ["energy", "solar", "renewable energy", "climate"],
    sourceNote: "Ember / Energy Institute",
  },
  "1134939": {
    name: "Renewables Share of Electricity (%)",
    description:
      "Percentage of total electricity generation from all renewable sources including hydro, solar, wind, and bioenergy",
    topics: ["energy", "renewable energy", "climate", "electricity"],
    sourceNote: "Ember / Energy Institute",
  },
  "1134910": {
    name: "Low-Carbon Electricity Share (%)",
    description:
      "Percentage of total electricity generation from low-carbon sources including nuclear and all renewables",
    topics: ["energy", "climate", "nuclear", "renewable energy"],
    sourceNote: "Ember / Energy Institute",
  },
  "819727": {
    name: "Share of Population in Extreme Poverty ($2.15/day)",
    description:
      "Percentage of population living below the international poverty line of $2.15 per day (2017 PPP)",
    topics: ["poverty", "development", "inequality", "economics"],
    sourceNote: "World Bank Poverty and Inequality Platform",
  },
  "899947": {
    name: "People Affected by Natural Disasters (per 100,000)",
    description:
      "Total number of people affected by all types of natural disasters per 100,000 population",
    topics: ["disasters", "climate", "vulnerability", "resilience"],
    sourceNote: "EM-DAT International Disaster Database",
  },
  "1134935": {
    name: "Electricity Consumption per Capita (kWh)",
    description:
      "Total electricity consumption per person in kilowatt-hours",
    topics: ["energy", "electricity", "development", "consumption"],
    sourceNote: "Ember / Energy Institute",
  },
  "899461": {
    name: "Ocean Heat Content (0-700m layer)",
    description:
      "Annual average ocean heat content for the upper 700 meters, a key indicator of global warming",
    topics: ["climate", "ocean", "warming", "environment"],
    sourceNote: "NOAA",
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
