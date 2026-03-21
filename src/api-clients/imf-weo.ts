import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://www.imf.org/external/datamapper/api/v1";

// Common IMF WEO indicator codes and their descriptions
const KNOWN_INDICATORS: Record<string, { name: string; description: string; topics: string[] }> = {
  NGDP_RPCH: { name: "Real GDP Growth", description: "Annual percent change of real gross domestic product", topics: ["economics", "growth"] },
  PCPIPCH: { name: "Inflation Rate (CPI)", description: "Annual percent change of consumer price index", topics: ["economics", "inflation"] },
  LUR: { name: "Unemployment Rate", description: "Percent of total labor force", topics: ["economics", "labor", "employment"] },
  GGXWDG_NGDP: { name: "Government Gross Debt (% of GDP)", description: "General government gross debt as percent of GDP", topics: ["economics", "debt", "government"] },
  BCA_NGDPD: { name: "Current Account Balance (% of GDP)", description: "Current account balance as percent of GDP", topics: ["economics", "trade"] },
  NGDPDPC: { name: "GDP per Capita (Current Prices)", description: "Gross domestic product per capita in current US dollars", topics: ["economics", "development"] },
  PPPPC: { name: "GDP per Capita (PPP)", description: "GDP per capita based on purchasing power parity in current international dollars", topics: ["economics", "development"] },
  NGDP_D: { name: "GDP Deflator", description: "Inflation measured by annual percent change of GDP deflator", topics: ["economics", "inflation"] },
  GGR_NGDP: { name: "Government Revenue (% of GDP)", description: "General government revenue as percent of GDP", topics: ["economics", "government"] },
  GGX_NGDP: { name: "Government Expenditure (% of GDP)", description: "General government total expenditure as percent of GDP", topics: ["economics", "government"] },
  GGXCNL_NGDP: { name: "Government Net Lending/Borrowing (% of GDP)", description: "General government net lending/borrowing as percent of GDP", topics: ["economics", "government"] },
  PCPIEPCH: { name: "Energy Inflation Rate", description: "Annual percent change of energy consumer price index", topics: ["economics", "inflation", "energy"] },
  LP: { name: "Population", description: "Total population in millions", topics: ["demographics", "population"] },
  TM_RPCH: { name: "Import Volume Growth", description: "Volume of imports of goods and services percent change", topics: ["economics", "trade"] },
  TX_RPCH: { name: "Export Volume Growth", description: "Volume of exports of goods and services percent change", topics: ["economics", "trade"] },
};

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`IMF API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  const results = Object.entries(KNOWN_INDICATORS)
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
      source: "IMF World Economic Outlook",
      topics: info.topics,
    }));

  // Also try to fetch the indicator list from the API for broader search
  if (results.length < limit) {
    try {
      const data = await fetchJSON<Record<string, Record<string, { label: string; description?: string }>>>(
        `${BASE}/indicators`
      );
      const indicators = data.indicators ?? {};
      for (const [code, info] of Object.entries(indicators)) {
        if (results.length >= limit) break;
        if (results.some(r => r.id === code)) continue;
        const label = info.label ?? code;
        if (label.toLowerCase().includes(q) || code.toLowerCase().includes(q)) {
          results.push({
            id: code,
            name: label,
            description: info.description ?? label,
            source: "IMF World Economic Outlook",
            topics: ["economics"],
          });
        }
      }
    } catch {
      // API indicator list may not be available; rely on known indicators
    }
  }

  return results;
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  // IMF API returns: { values: { INDICATOR: { COUNTRY_CODE: { YEAR: VALUE } } } }
  const url = `${BASE}/${indicatorId}`;
  const response = await fetchJSON<{
    values: Record<string, Record<string, Record<string, number>>>;
  }>(url);

  const indicatorData = response.values?.[indicatorId];
  if (!indicatorData) {
    return { name: indicatorId, data: [] };
  }

  const name = KNOWN_INDICATORS[indicatorId]?.name ?? indicatorId;
  const countryFilter = countries?.split(",").map(c => c.trim().toUpperCase());

  // Fetch country name mapping
  let countryNames: Record<string, string> = {};
  try {
    const countriesData = await fetchJSON<{ countries: Record<string, { label: string }> }>(
      `${BASE}/countries`
    );
    for (const [code, info] of Object.entries(countriesData.countries ?? {})) {
      countryNames[code] = info.label;
    }
  } catch {
    // Fall back to using codes as names
  }

  const data: DataPoint[] = [];
  for (const [countryCode, yearValues] of Object.entries(indicatorData)) {
    // Skip aggregate regions (they tend to have longer codes or special patterns)
    if (countryCode.length !== 3) continue;
    if (countryFilter && !countryFilter.includes(countryCode.toUpperCase())) continue;

    for (const [year, value] of Object.entries(yearValues)) {
      const yearNum = parseInt(year, 10);
      if (isNaN(yearNum) || value === null || value === undefined) continue;
      data.push({
        country: countryCode.toUpperCase(),
        countryName: countryNames[countryCode] ?? countryCode,
        year: yearNum,
        value: typeof value === "number" ? value : null,
      });
    }
  }

  data.sort((a, b) => a.year - b.year);
  return { name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return `https://www.imf.org/external/datamapper/${indicatorId}`;
}
