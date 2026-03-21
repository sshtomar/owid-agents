import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://fenixservices.fao.org/faostat/api/v1/en";

// FAO domain codes and common indicators
// Format: DOMAIN_CODE.ELEMENT_CODE.ITEM_CODE
const KNOWN_INDICATORS: Record<string, { name: string; description: string; domain: string; element: string; item: string; topics: string[] }> = {
  "QCL.5510.15": { name: "Wheat Production", description: "Annual wheat production in tonnes", domain: "QCL", element: "5510", item: "15", topics: ["agriculture", "food", "production"] },
  "QCL.5510.27": { name: "Rice Production", description: "Annual paddy rice production in tonnes", domain: "QCL", element: "5510", item: "27", topics: ["agriculture", "food", "production"] },
  "QCL.5510.56": { name: "Maize (Corn) Production", description: "Annual maize production in tonnes", domain: "QCL", element: "5510", item: "56", topics: ["agriculture", "food", "production"] },
  "QCL.5510.236": { name: "Soybean Production", description: "Annual soybean production in tonnes", domain: "QCL", element: "5510", item: "236", topics: ["agriculture", "food", "production"] },
  "QCL.5510.656": { name: "Coffee Production", description: "Annual coffee (green) production in tonnes", domain: "QCL", element: "5510", item: "656", topics: ["agriculture", "food", "production", "commodities"] },
  "QCL.5510.661": { name: "Cocoa Bean Production", description: "Annual cocoa bean production in tonnes", domain: "QCL", element: "5510", item: "661", topics: ["agriculture", "food", "production", "commodities"] },
  "QCL.5510.572": { name: "Sugarcane Production", description: "Annual sugarcane production in tonnes", domain: "QCL", element: "5510", item: "572", topics: ["agriculture", "food", "production"] },
  "QCL.5312.866": { name: "Cattle Stock", description: "Number of cattle (livestock units)", domain: "QCL", element: "5312", item: "866", topics: ["agriculture", "livestock"] },
  "QCL.5510.388": { name: "Tomato Production", description: "Annual tomato production in tonnes", domain: "QCL", element: "5510", item: "388", topics: ["agriculture", "food", "production"] },
  "RL.5110.6621": { name: "Agricultural Land", description: "Agricultural land area in 1000 hectares", domain: "RL", element: "5110", item: "6621", topics: ["agriculture", "land use", "environment"] },
  "RL.5110.6661": { name: "Forest Land", description: "Forest land area in 1000 hectares", domain: "RL", element: "5110", item: "6661", topics: ["environment", "land use", "forestry"] },
  "FBS.664.2501": { name: "Food Supply (kcal/capita/day)", description: "Dietary energy supply in kilocalories per person per day", domain: "FBS", element: "664", item: "2501", topics: ["food security", "nutrition", "health"] },
  "EI.7273.6842": { name: "CO2 Emissions from Agriculture", description: "Carbon dioxide emissions from agriculture in kilotonnes", domain: "EI", element: "7273", item: "6842", topics: ["environment", "climate", "emissions", "agriculture"] },
};

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`FAO API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

// FAO uses its own area codes; we need to map M49 codes to ISO3
async function getAreaMapping(): Promise<Record<string, { iso3: string; name: string }>> {
  try {
    const data = await fetchJSON<{ data: Array<{ "Country Code": string; "ISO3 Code": string; Country: string }> }>(
      `${BASE}/definitions/types/areagroup/1`
    );
    const mapping: Record<string, { iso3: string; name: string }> = {};
    for (const item of data.data ?? []) {
      if (item["ISO3 Code"]) {
        mapping[item["Country Code"]] = {
          iso3: item["ISO3 Code"],
          name: item.Country,
        };
      }
    }
    return mapping;
  } catch {
    return {};
  }
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  return Object.entries(KNOWN_INDICATORS)
    .filter(([code, info]) =>
      code.toLowerCase().includes(q) ||
      info.name.toLowerCase().includes(q) ||
      info.description.toLowerCase().includes(q) ||
      info.topics.some(t => t.includes(q))
    )
    .slice(0, limit)
    .map(([code, info]) => ({
      id: code,
      name: info.name,
      description: info.description,
      source: "FAO FAOSTAT",
      topics: info.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = KNOWN_INDICATORS[indicatorId];
  if (!indicator) {
    // Try parsing the ID as DOMAIN.ELEMENT.ITEM
    const parts = indicatorId.split(".");
    if (parts.length !== 3) {
      throw new Error(`Unknown FAO indicator: ${indicatorId}. Use format: DOMAIN.ELEMENT.ITEM`);
    }
    return fetchFAOData(parts[0], parts[1], parts[2], indicatorId, countries);
  }

  return fetchFAOData(indicator.domain, indicator.element, indicator.item, indicator.name, countries);
}

async function fetchFAOData(
  domain: string,
  element: string,
  item: string,
  name: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  // Build year range
  const years = Array.from({ length: 65 }, (_, i) => 1960 + i).join(",");
  const areaParam = countries ? `&area=${countries}` : "";

  const url = `${BASE}/data/${domain}?element=${element}&item=${item}${areaParam}&year=${years}&area_cs=ISO3&show_codes=true&show_flags=true&output_type=objects`;

  let responseData: Array<{ Area: string; "Area Code (ISO3)": string; Year: number; Value: number | null }>;
  try {
    const response = await fetchJSON<{ data: typeof responseData }>(url);
    responseData = response.data ?? [];
  } catch {
    // Try with M49 area codes and map them
    const urlM49 = `${BASE}/data/${domain}?element=${element}&item=${item}${areaParam}&year=${years}&area_cs=M49&show_codes=true&show_flags=true&output_type=objects`;
    try {
      const response = await fetchJSON<{ data: Array<{ Area: string; "Area Code (M49)": string; Year: number; Value: number | null }> }>(urlM49);
      const areaMapping = await getAreaMapping();
      responseData = (response.data ?? []).map(d => ({
        ...d,
        "Area Code (ISO3)": areaMapping[d["Area Code (M49)"]]?.iso3 ?? d["Area Code (M49)"],
      }));
    } catch {
      return { name, data: [] };
    }
  }

  const data: DataPoint[] = responseData
    .filter(d => d.Value !== null && d.Value !== undefined)
    .map(d => ({
      country: d["Area Code (ISO3)"] ?? d.Area?.slice(0, 3) ?? "UNK",
      countryName: d.Area ?? "Unknown",
      year: d.Year,
      value: d.Value,
    }))
    .sort((a, b) => a.year - b.year);

  return { name, data };
}

export function getSourceUrl(indicatorId: string): string {
  const parts = indicatorId.split(".");
  const domain = parts[0] ?? "QCL";
  return `https://www.fao.org/faostat/en/#data/${domain}`;
}
