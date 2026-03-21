import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://api.unhcr.org/population/v1";

// Available population type fields in the UNHCR API
const INDICATORS: Record<
  string,
  { name: string; field: string; description: string; topics: string[] }
> = {
  refugees: {
    name: "Refugees by Country of Origin",
    field: "refugees",
    description:
      "Number of refugees originating from each country, recognized under international law",
    topics: ["refugees", "displacement", "conflict"],
  },
  refugees_asylum: {
    name: "Refugees by Country of Asylum",
    field: "refugees",
    description:
      "Number of refugees hosted by each country of asylum",
    topics: ["refugees", "displacement", "migration"],
  },
  idps: {
    name: "Internally Displaced Persons",
    field: "idps",
    description:
      "People forced to flee within their own country due to conflict or violence",
    topics: ["displacement", "conflict"],
  },
  asylum_seekers: {
    name: "Asylum Seekers by Country of Asylum",
    field: "asylum_seekers",
    description: "People who have applied for international protection but whose claim has not yet been determined",
    topics: ["refugees", "asylum", "migration"],
  },
  stateless: {
    name: "Stateless Persons",
    field: "stateless",
    description:
      "People who are not considered nationals by any state under its law",
    topics: ["statelessness", "human rights"],
  },
};

interface UNHCRRecord {
  year: number;
  coo_name: string;
  coo: string;
  coa_name: string;
  coa: string;
  refugees: number;
  asylum_seekers: number;
  idps: number;
  stateless: string | number;
  [key: string]: string | number;
}

interface UNHCRResponse {
  items: UNHCRRecord[];
  totalItems: number;
  nextPage?: string;
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`UNHCR API error: ${res.status} ${res.statusText}`);
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
        v.topics.some((t) => t.includes(q))
    )
    .slice(0, limit)
    .map(([id, v]) => ({
      id,
      name: v.name,
      description: v.description,
      source: "UNHCR",
      topics: v.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];
  if (!indicator) {
    throw new Error(`Unknown UNHCR indicator: ${indicatorId}`);
  }

  // Determine if we're grouping by country of origin or asylum
  const isAsylumBased = indicatorId.endsWith("_asylum");
  const countryParam = isAsylumBased ? "coa" : "coo";
  const countryNameField = isAsylumBased ? "coa_name" : "coo_name";
  const countryCodeField = isAsylumBased ? "coa" : "coo";

  let url = `${BASE}/population/?limit=10000&yearFrom=2000&yearTo=2024&${countryParam}_all=true`;
  if (countries) {
    url += `&${countryParam}=${countries}`;
  }

  const response = await fetchJSON<UNHCRResponse>(url);

  // Aggregate by country + year
  const aggregated = new Map<string, DataPoint>();

  for (const record of response.items) {
    const code = record[countryCodeField] as string;
    const name = record[countryNameField] as string;
    const year = record.year;
    const rawValue = record[indicator.field];
    const value =
      typeof rawValue === "string" ? parseFloat(rawValue) : rawValue;

    if (!code || !year || isNaN(value as number)) continue;

    const key = `${code}-${year}`;
    const existing = aggregated.get(key);
    if (existing) {
      existing.value = (existing.value ?? 0) + (value as number);
    } else {
      aggregated.set(key, {
        country: code,
        countryName: name,
        year,
        value: value as number,
      });
    }
  }

  const data = [...aggregated.values()]
    .filter((d) => d.value !== null && d.value > 0)
    .sort((a, b) => a.year - b.year);

  return { name: indicator.name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return "https://www.unhcr.org/refugee-statistics/";
}
