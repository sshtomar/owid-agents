import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://api.eia.gov/v2/international/data/";

function getApiKey(): string {
  const key = process.env.EIA_API_KEY;
  if (!key) {
    throw new Error(
      "EIA_API_KEY environment variable is not set. " +
        "Get a free API key at https://www.eia.gov/opendata/register.php"
    );
  }
  return key;
}

// activityId: 2 = net generation (billion kWh), 7 = installed capacity (million kW)
// productId maps to fuel/technology type
interface IndicatorDef {
  name: string;
  activityId: number;
  productId: number;
  unit: string;
  topics: string[];
}

const INDICATORS: Record<string, IndicatorDef> = {
  // Generation (activityId 2)
  "INTL-GEN-SOLAR": {
    name: "Solar electricity net generation (billion kWh)",
    activityId: 2,
    productId: 29,
    unit: "billion kWh",
    topics: ["energy", "renewable", "solar", "electricity"],
  },
  "INTL-GEN-WIND": {
    name: "Wind electricity net generation (billion kWh)",
    activityId: 2,
    productId: 27,
    unit: "billion kWh",
    topics: ["energy", "renewable", "wind", "electricity"],
  },
  "INTL-GEN-NUCLEAR": {
    name: "Nuclear electricity net generation (billion kWh)",
    activityId: 2,
    productId: 2,
    unit: "billion kWh",
    topics: ["energy", "nuclear", "electricity"],
  },
  "INTL-GEN-HYDRO": {
    name: "Hydroelectricity net generation (billion kWh)",
    activityId: 2,
    productId: 6,
    unit: "billion kWh",
    topics: ["energy", "renewable", "hydro", "electricity"],
  },
  "INTL-GEN-COAL": {
    name: "Coal electricity net generation (billion kWh)",
    activityId: 2,
    productId: 36,
    unit: "billion kWh",
    topics: ["energy", "fossil", "coal", "electricity"],
  },
  "INTL-GEN-GAS": {
    name: "Natural gas electricity net generation (billion kWh)",
    activityId: 2,
    productId: 37,
    unit: "billion kWh",
    topics: ["energy", "fossil", "gas", "electricity"],
  },
  "INTL-GEN-OIL": {
    name: "Petroleum electricity net generation (billion kWh)",
    activityId: 2,
    productId: 38,
    unit: "billion kWh",
    topics: ["energy", "fossil", "oil", "electricity"],
  },
  "INTL-GEN-GEOTHERMAL": {
    name: "Geothermal electricity net generation (billion kWh)",
    activityId: 2,
    productId: 33,
    unit: "billion kWh",
    topics: ["energy", "renewable", "geothermal", "electricity"],
  },
  "INTL-GEN-BIOMASS": {
    name: "Biomass and waste electricity net generation (billion kWh)",
    activityId: 2,
    productId: 35,
    unit: "billion kWh",
    topics: ["energy", "renewable", "biomass", "electricity"],
  },
  "INTL-GEN-TOTAL": {
    name: "Total electricity net generation (billion kWh)",
    activityId: 2,
    productId: 79,
    unit: "billion kWh",
    topics: ["energy", "electricity"],
  },
  // Capacity (activityId 7)
  "INTL-CAP-SOLAR": {
    name: "Solar installed electricity capacity (million kW)",
    activityId: 7,
    productId: 29,
    unit: "million kW",
    topics: ["energy", "renewable", "solar", "capacity"],
  },
  "INTL-CAP-WIND": {
    name: "Wind installed electricity capacity (million kW)",
    activityId: 7,
    productId: 27,
    unit: "million kW",
    topics: ["energy", "renewable", "wind", "capacity"],
  },
  "INTL-CAP-NUCLEAR": {
    name: "Nuclear installed electricity capacity (million kW)",
    activityId: 7,
    productId: 2,
    unit: "million kW",
    topics: ["energy", "nuclear", "capacity"],
  },
  "INTL-CAP-HYDRO": {
    name: "Hydroelectricity installed capacity (million kW)",
    activityId: 7,
    productId: 6,
    unit: "million kW",
    topics: ["energy", "renewable", "hydro", "capacity"],
  },
  "INTL-CAP-TOTAL": {
    name: "Total installed electricity capacity (million kW)",
    activityId: 7,
    productId: 79,
    unit: "million kW",
    topics: ["energy", "capacity"],
  },
};

interface EiaRow {
  period: number;
  activityId: number;
  activityName: string;
  productId: number;
  productName: string;
  countryRegionId: string;
  countryRegionName: string;
  unit: string;
  unitName: string;
  value: number | string | null;
}

interface EiaApiResponse {
  response: {
    total: number;
    data: EiaRow[];
  };
}

const MAX_LENGTH = 5000;

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`EIA API error: ${res.status} ${res.statusText} - ${body}`);
  }
  return res.json() as Promise<T>;
}

// Fetch all pages of data for a given indicator, handling the 5000-row limit.
async function fetchAllRows(
  indicator: IndicatorDef,
  countries?: string[]
): Promise<EiaRow[]> {
  const apiKey = getApiKey();
  const allRows: EiaRow[] = [];
  let offset = 0;

  // eslint-disable-next-line no-constant-condition
  while (true) {
    const params = new URLSearchParams();
    params.set("api_key", apiKey);
    params.set("data[]", "value");
    params.append("facets[activityId][]", String(indicator.activityId));
    params.append("facets[productId][]", String(indicator.productId));
    params.set("frequency", "annual");
    params.set("offset", String(offset));
    params.set("length", String(MAX_LENGTH));

    if (countries) {
      for (const c of countries) {
        params.append("facets[countryRegionId][]", c);
      }
    }

    const url = `${BASE}?${params.toString()}`;
    const result = await fetchJSON<EiaApiResponse>(url);
    const rows = result.response.data;
    allRows.push(...rows);

    if (allRows.length >= result.response.total || rows.length < MAX_LENGTH) {
      break;
    }
    offset += MAX_LENGTH;
  }

  return allRows;
}

// Country-level records use 3-character ISO codes.
// Longer codes (e.g. "WORL", "AFRC") are regional aggregates.
function isCountryRecord(row: EiaRow): boolean {
  return row.countryRegionId.length <= 3;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  return Object.entries(INDICATORS)
    .filter(([id, ind]) => {
      const haystack = `${id} ${ind.name} ${ind.topics.join(" ")}`.toLowerCase();
      return q.split(/\s+/).every((word) => haystack.includes(word));
    })
    .slice(0, limit)
    .map(([id, ind]) => ({
      id,
      name: ind.name,
      description: `EIA international energy data: ${ind.name}`,
      source: "EIA",
      topics: ind.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];
  if (!indicator) {
    throw new Error(
      `Unknown EIA indicator: ${indicatorId}. Use searchIndicators() to find valid IDs.`
    );
  }

  const countryList = countries
    ? countries.split(",").map((c) => c.trim().toUpperCase())
    : undefined;

  const rows = await fetchAllRows(indicator, countryList);

  const data: DataPoint[] = [];
  for (const row of rows) {
    if (!isCountryRecord(row)) continue;

    const numValue =
      typeof row.value === "number"
        ? row.value
        : typeof row.value === "string"
          ? parseFloat(row.value)
          : null;

    if (numValue === null || isNaN(numValue)) continue;

    data.push({
      country: row.countryRegionId,
      countryName: row.countryRegionName,
      year: typeof row.period === "number" ? row.period : parseInt(String(row.period), 10),
      value: numValue,
    });
  }

  data.sort((a, b) => a.year - b.year);
  return { name: indicator.name, data };
}

export function getSourceUrl(indicatorId: string): string {
  const indicator = INDICATORS[indicatorId];
  if (!indicator) {
    return "https://www.eia.gov/opendata/browser/?frequency=annual&data=value&facets=activityId%3B&sortColumn=period&sortDirection=desc";
  }
  return (
    `https://www.eia.gov/opendata/browser/?frequency=annual&data=value` +
    `&facets=activityId%3B${indicator.activityId}%3BproductId%3B${indicator.productId}` +
    `&sortColumn=period&sortDirection=desc`
  );
}
