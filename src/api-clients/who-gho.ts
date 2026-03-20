import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://ghoapi.azureedge.net/api";

interface GHOIndicator {
  IndicatorCode: string;
  IndicatorName: string;
  Language: string;
}

interface GHODataPoint {
  SpatialDim: string;
  TimeDim: string;
  NumericValue: number | null;
  Value: string;
}

interface GHOResponse<T> {
  value: T[];
  "@odata.nextLink"?: string;
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`WHO GHO API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const url = `${BASE}/Indicator?$filter=contains(tolower(IndicatorName),tolower('${encodeURIComponent(query)}'))&$top=${limit}`;
  const data = await fetchJSON<GHOResponse<GHOIndicator>>(url);

  return data.value
    .filter((ind) => ind.Language === "EN")
    .map((ind) => ({
      id: ind.IndicatorCode,
      name: ind.IndicatorName,
      description: "",
      source: "WHO Global Health Observatory",
      topics: [],
    }));
}

export async function fetchIndicatorData(
  indicatorCode: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  let url = `${BASE}/${indicatorCode}?$top=1000`;
  if (countries) {
    const codes = countries.split(",").map((c) => `SpatialDim eq '${c.trim()}'`);
    url += `&$filter=${codes.join(" or ")}`;
  }

  // Paginate through all results
  const allValues: GHODataPoint[] = [];
  let nextUrl: string | undefined = url;
  while (nextUrl) {
    const page = await fetchJSON<GHOResponse<GHODataPoint>>(nextUrl);
    allValues.push(...page.value);
    nextUrl = page["@odata.nextLink"];
  }
  const response = { value: allValues };

  // Get indicator name
  const metaUrl = `${BASE}/Indicator?$filter=IndicatorCode eq '${indicatorCode}'`;
  const meta = await fetchJSON<GHOResponse<GHOIndicator>>(metaUrl);
  const name =
    meta.value.find((i) => i.Language === "EN")?.IndicatorName ?? indicatorCode;

  // Country name lookup is not available in GHO API directly,
  // so we use the ISO3 code as both code and name placeholder
  const data: DataPoint[] = response.value
    .filter((d) => d.NumericValue !== null && d.TimeDim)
    .map((d) => ({
      country: d.SpatialDim,
      countryName: d.SpatialDim,
      year: parseInt(d.TimeDim, 10),
      value: d.NumericValue,
    }))
    .filter((d) => !isNaN(d.year))
    .sort((a, b) => a.year - b.year);

  return { name, data };
}

export function getSourceUrl(indicatorCode: string): string {
  return `https://www.who.int/data/gho/data/indicators/indicator-details/GHO/${indicatorCode}`;
}
