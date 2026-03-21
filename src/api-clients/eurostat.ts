import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE =
  "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data";

// Curated catalog of interesting Eurostat datasets with their dimension filters
interface EurostatDataset {
  code: string;
  name: string;
  description: string;
  topics: string[];
  // Dimension filters to apply (vary per dataset)
  filters: Record<string, string>;
}

const DATASETS: EurostatDataset[] = [
  {
    code: "demo_pjan",
    name: "Population on 1 January",
    description: "Total population by country on January 1st each year",
    topics: ["demographics", "population"],
    filters: { age: "TOTAL", sex: "T" },
  },
  {
    code: "demo_mlexpec",
    name: "Life Expectancy by Age and Sex",
    description: "Life expectancy at birth and other ages in EU countries",
    topics: ["health", "demographics"],
    filters: { age: "Y_LT1", sex: "T" },
  },
  {
    code: "sdg_07_40",
    name: "Share of Renewable Energy",
    description:
      "Share of renewable energy in gross final energy consumption (%)",
    topics: ["energy", "environment", "climate"],
    filters: { nrg_bal: "REN", unit: "PC" },
  },
  {
    code: "sdg_13_10",
    name: "Greenhouse Gas Emissions",
    description:
      "Net greenhouse gas emissions (tonnes per capita, excluding LULUCF)",
    topics: ["climate", "environment"],
    filters: { src_crf: "TOTX4_MEMO", unit: "T_HAB" },
  },
  {
    code: "sdg_01_10",
    name: "People at Risk of Poverty or Social Exclusion",
    description: "Share of population at risk of poverty or social exclusion",
    topics: ["poverty", "social"],
    filters: {},
  },
  {
    code: "sdg_04_10",
    name: "Early Leavers from Education and Training",
    description:
      "Share of early leavers from education and training (18-24 year olds)",
    topics: ["education"],
    filters: { sex: "T" },
  },
  {
    code: "sdg_05_20",
    name: "Gender Pay Gap",
    description: "Gender pay gap in unadjusted form (%)",
    topics: ["gender", "economics", "labor"],
    filters: { nace_r2: "B-S_X_O" },
  },
  {
    code: "sdg_08_10",
    name: "Real GDP per Capita",
    description: "Real GDP per capita in chain linked volumes",
    topics: ["economics", "development"],
    filters: { na_item: "B1GQ" },
  },
  {
    code: "sdg_03_41",
    name: "Causes of Death - Standardised Death Rate",
    description: "Standardised death rate by causes of death",
    topics: ["health", "mortality"],
    filters: { sex: "T", icd10: "A-R_V-Y" },
  },
  {
    code: "sdg_09_40",
    name: "Share of Rail and Inland Waterways in Freight Transport",
    description: "Share of rail and inland waterways in total freight transport",
    topics: ["transport", "infrastructure"],
    filters: {},
  },
  {
    code: "sdg_11_60",
    name: "Population Exposed to Air Pollution (PM2.5)",
    description:
      "Population living in households exposed to pollution by particulate matter",
    topics: ["environment", "health", "air quality"],
    filters: {},
  },
  {
    code: "sdg_06_40",
    name: "Water Exploitation Index",
    description: "Water exploitation index plus (WEI+)",
    topics: ["water", "environment"],
    filters: {},
  },
  {
    code: "sdg_02_10",
    name: "Obesity Rate",
    description: "Proportion of overweight/obese population (BMI >= 25)",
    topics: ["health", "nutrition"],
    filters: { bmi: "BMI_GE25", sex: "T", age: "TOTAL" },
  },
  {
    code: "une_rt_m",
    name: "Unemployment Rate - Monthly",
    description: "Harmonised unemployment rates by sex, seasonally adjusted",
    topics: ["labor", "economics"],
    filters: { s_adj: "SA", age: "TOTAL", sex: "T", unit: "PC_ACT" },
  },
  {
    code: "migr_imm1ctz",
    name: "Immigration by Citizenship",
    description: "Immigration by age group, sex and citizenship",
    topics: ["migration", "demographics"],
    filters: { age: "TOTAL", sex: "T", citizen: "NEU27_2020_FOR" },
  },
];

interface EurostatResponse {
  label: string;
  id: string[];
  size: number[];
  value: Record<string, number>;
  dimension: Record<
    string,
    {
      label: string;
      category: {
        index: Record<string, number>;
        label: Record<string, string>;
      };
    }
  >;
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Eurostat API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  return DATASETS.filter(
    (ds) =>
      ds.name.toLowerCase().includes(q) ||
      ds.description.toLowerCase().includes(q) ||
      ds.topics.some((t) => t.includes(q))
  )
    .slice(0, limit)
    .map((ds) => ({
      id: ds.code,
      name: ds.name,
      description: ds.description,
      source: "Eurostat",
      topics: ds.topics,
    }));
}

function decodeJsonStat(response: EurostatResponse): DataPoint[] {
  const dimIds = response.id;
  const sizes = response.size;

  // Find geo and time dimension indices
  const geoIdx = dimIds.indexOf("geo");
  const timeIdx = dimIds.indexOf("time");
  if (geoIdx === -1 || timeIdx === -1) return [];

  const geoDim = response.dimension.geo;
  const timeDim = response.dimension.time;
  if (!geoDim || !timeDim) return [];

  const geoLabels = geoDim.category.label;
  const geoIndex = geoDim.category.index;
  const timeLabels = timeDim.category.label;
  const timeIndex = timeDim.category.index;

  // Build reverse lookup: position -> code
  const geoByPos: Record<number, string> = {};
  for (const [code, pos] of Object.entries(geoIndex)) {
    geoByPos[pos] = code;
  }
  const timeByPos: Record<number, string> = {};
  for (const [code, pos] of Object.entries(timeIndex)) {
    timeByPos[pos] = code;
  }

  // Compute strides for each dimension
  const strides: number[] = new Array(dimIds.length);
  strides[dimIds.length - 1] = 1;
  for (let i = dimIds.length - 2; i >= 0; i--) {
    strides[i] = strides[i + 1] * sizes[i + 1];
  }

  const points: DataPoint[] = [];

  for (const [indexStr, value] of Object.entries(response.value)) {
    const index = parseInt(indexStr, 10);

    // Extract geo and time positions from the linear index
    const geoPos = Math.floor(index / strides[geoIdx]) % sizes[geoIdx];
    const timePos = Math.floor(index / strides[timeIdx]) % sizes[timeIdx];

    const geoCode = geoByPos[geoPos];
    const timeCode = timeByPos[timePos];
    if (!geoCode || !timeCode) continue;

    // Skip aggregate regions (keep 2-letter country codes only)
    if (geoCode.length > 2) continue;

    const year = parseInt(timeCode, 10);
    if (isNaN(year)) continue;

    points.push({
      country: geoCode,
      countryName: geoLabels[geoCode] ?? geoCode,
      year,
      value,
    });
  }

  return points.sort((a, b) => a.year - b.year);
}

export async function fetchIndicatorData(
  datasetCode: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const dataset = DATASETS.find((ds) => ds.code === datasetCode);

  // Build URL with dimension filters
  const params = new URLSearchParams({
    format: "JSON",
    lang: "EN",
    sinceTimePeriod: "1990",
  });

  if (countries) {
    params.set("geo", countries);
  }

  // Apply dataset-specific filters
  if (dataset) {
    for (const [key, val] of Object.entries(dataset.filters)) {
      params.set(key, val);
    }
  }

  const url = `${BASE}/${datasetCode}?${params}`;
  const response = await fetchJSON<EurostatResponse>(url);

  const name = response.label || dataset?.name || datasetCode;
  const data = decodeJsonStat(response);

  return { name, data };
}

export function getSourceUrl(datasetCode: string): string {
  return `https://ec.europa.eu/eurostat/databrowser/view/${datasetCode}/default/table`;
}
