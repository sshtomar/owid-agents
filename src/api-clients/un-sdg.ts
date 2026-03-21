import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg";

interface SDGIndicator {
  goal: string;
  target: string;
  code: string;
  description: string;
  series: Array<{
    code: string;
    description: string;
  }>;
}

interface SDGDataRecord {
  geoAreaCode: string;
  geoAreaName: string;
  timePeriodStart: number;
  value: string;
  series: string;
  seriesDescription: string;
}

interface SDGDataResponse {
  totalElements: number;
  totalPages: number;
  pageNumber: number;
  data: SDGDataRecord[];
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`UN SDG API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

let indicatorCache: SDGIndicator[] | null = null;

async function loadIndicators(): Promise<SDGIndicator[]> {
  if (indicatorCache) return indicatorCache;
  indicatorCache = await fetchJSON<SDGIndicator[]>(`${BASE}/Indicator/List`);
  return indicatorCache;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const indicators = await loadIndicators();
  const q = query.toLowerCase();

  const matches: IndicatorSearchResult[] = [];

  for (const ind of indicators) {
    if (matches.length >= limit) break;

    const descMatch = ind.description.toLowerCase().includes(q);
    const seriesMatch = ind.series.some((s) =>
      s.description.toLowerCase().includes(q)
    );

    if (descMatch || seriesMatch) {
      // Use the first series code as the indicator ID for fetching
      const primarySeries = ind.series[0];
      if (!primarySeries) continue;

      matches.push({
        id: `${ind.code}::${primarySeries.code}`,
        name: primarySeries.description,
        description: `SDG ${ind.goal} Target ${ind.target}: ${ind.description.slice(0, 150)}`,
        source: "UN Sustainable Development Goals",
        topics: [`sdg-${ind.goal}`],
      });
    }
  }

  return matches;
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  // indicatorId format: "1.1.1::SI_POV_DAY1" (indicator code :: series code)
  const [indCode, seriesCode] = indicatorId.split("::");
  if (!indCode || !seriesCode) {
    throw new Error(
      `Invalid indicator ID format. Expected "indicator::series", got "${indicatorId}"`
    );
  }

  // Fetch country-level data only, paginate through results
  const allData: SDGDataRecord[] = [];
  let page = 1;
  const pageSize = 1000;

  while (true) {
    let url = `${BASE}/Indicator/Data?indicator=${indCode}&pageSize=${pageSize}&page=${page}&areaType=country`;
    if (countries) {
      const codes = countries.split(",").map((c) => c.trim());
      url += `&geoAreaCode=${codes.join(",")}`;
    }

    const response = await fetchJSON<SDGDataResponse>(url);
    // Filter to the specific series locally (seriescode param causes 500s)
    const filtered = response.data.filter((d) => d.series === seriesCode);
    allData.push(...filtered);

    if (page >= response.totalPages || allData.length >= 10000) break;
    page++;
  }

  // Get indicator name from the series description
  const name =
    allData[0]?.seriesDescription ?? `SDG ${indCode} (${seriesCode})`;

  // Filter to aggregate dimensions only (ALLAGE, BOTHSEX, etc.) to avoid duplicates
  const data: DataPoint[] = allData
    .filter((d) => {
      const val = parseFloat(d.value);
      return !isNaN(val) && d.geoAreaCode && d.timePeriodStart;
    })
    .map((d) => ({
      country: d.geoAreaCode,
      countryName: d.geoAreaName,
      year: d.timePeriodStart,
      value: parseFloat(d.value),
    }))
    .sort((a, b) => a.year - b.year);

  // Deduplicate: keep latest value per country-year pair
  const seen = new Map<string, DataPoint>();
  for (const d of data) {
    const key = `${d.country}-${d.year}`;
    seen.set(key, d);
  }

  return { name, data: [...seen.values()].sort((a, b) => a.year - b.year) };
}

export function getSourceUrl(indicatorId: string): string {
  const [indCode] = indicatorId.split("::");
  return `https://unstats.un.org/sdgs/dataportal/database`;
}
