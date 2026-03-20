import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://api.worldbank.org/v2";

interface WBIndicator {
  id: string;
  name: string;
  sourceNote: string;
  source: { value: string };
  topics: Array<{ value: string }>;
}

interface WBDataPoint {
  country: { id: string; value: string };
  date: string;
  value: number | null;
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`World Bank API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const url = `${BASE}/indicator?format=json&per_page=${limit}&source=2&search=${encodeURIComponent(query)}`;
  const data = await fetchJSON<[unknown, WBIndicator[]]>(url);

  if (!data[1]) return [];

  return data[1].map((ind) => ({
    id: ind.id,
    name: ind.name,
    description: ind.sourceNote?.slice(0, 200) ?? "",
    source: ind.source?.value ?? "World Bank",
    topics: ind.topics
      ?.filter((t) => t.value?.trim())
      .map((t) => t.value.trim()) ?? [],
  }));
}

export async function searchByTopic(
  topic: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  // Search indicators matching the topic keyword
  return searchIndicators(topic, limit);
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string,
  perPage = 10000
): Promise<{ name: string; data: DataPoint[] }> {
  // Use specific countries or default to actual country codes (exclude aggregates)
  const countryParam = countries ?? "all";
  const url = `${BASE}/country/${countryParam}/indicator/${indicatorId}?format=json&per_page=${perPage}&date=1960:2024`;
  const response = await fetchJSON<[{ total: number }, WBDataPoint[] | null]>(url);

  if (!response[1]) {
    return { name: indicatorId, data: [] };
  }

  // Get indicator name from a separate call
  const metaUrl = `${BASE}/indicator/${indicatorId}?format=json`;
  const meta = await fetchJSON<[unknown, WBIndicator[]]>(metaUrl);
  const name = meta[1]?.[0]?.name ?? indicatorId;

  const data: DataPoint[] = response[1]
    .filter((d) => d.value !== null)
    .map((d) => ({
      country: d.country.id,
      countryName: d.country.value,
      year: parseInt(d.date, 10),
      value: d.value,
    }))
    .sort((a, b) => a.year - b.year);

  return { name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return `https://data.worldbank.org/indicator/${indicatorId}`;
}
