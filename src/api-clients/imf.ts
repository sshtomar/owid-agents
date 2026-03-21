import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://www.imf.org/external/datamapper/api/v1";

// Curated set of interesting IMF indicators
const INDICATORS: Record<
  string,
  { name: string; description: string; topics: string[] }
> = {
  GGXWDG_NGDP: {
    name: "Government Gross Debt (% of GDP)",
    description:
      "General government gross debt as a percentage of GDP",
    topics: ["debt", "fiscal", "economics"],
  },
  HH_LS: {
    name: "Household Debt (% of GDP)",
    description:
      "Household debt (loans and debt securities) as a percentage of GDP",
    topics: ["debt", "households", "economics"],
  },
  Privatedebt_all: {
    name: "Private Sector Debt (% of GDP)",
    description:
      "Total private debt (all instruments) as a percentage of GDP",
    topics: ["debt", "finance", "economics"],
  },
  PCPIPCH: {
    name: "Inflation Rate (annual % change)",
    description:
      "Annual percentage change in average consumer prices",
    topics: ["inflation", "economics", "prices"],
  },
  LUR: {
    name: "Unemployment Rate (%)",
    description: "Unemployment rate as percentage of total labor force",
    topics: ["labor", "unemployment", "economics"],
  },
  NGDP_RPCH: {
    name: "Real GDP Growth (annual %)",
    description: "Annual percentage change of real GDP",
    topics: ["economics", "growth", "gdp"],
  },
  BCA_NGDPD: {
    name: "Current Account Balance (% of GDP)",
    description:
      "Current account balance as a percentage of GDP",
    topics: ["trade", "economics", "balance of payments"],
  },
  GGR_NGDP: {
    name: "Government Revenue (% of GDP)",
    description: "General government revenue as a percentage of GDP",
    topics: ["fiscal", "government", "economics"],
  },
  GGXCNL_NGDP: {
    name: "Government Net Lending/Borrowing (% of GDP)",
    description:
      "General government net lending/borrowing (fiscal balance) as % of GDP",
    topics: ["fiscal", "deficit", "economics"],
  },
  NFC_LS: {
    name: "Nonfinancial Corporate Debt (% of GDP)",
    description:
      "Nonfinancial corporate debt (loans and debt securities) as % of GDP",
    topics: ["debt", "corporate", "finance"],
  },
};

// ISO3 country code to name mapping for the most common ones
const COUNTRY_NAMES: Record<string, string> = {
  USA: "United States", GBR: "United Kingdom", DEU: "Germany",
  FRA: "France", JPN: "Japan", CHN: "China", IND: "India",
  BRA: "Brazil", RUS: "Russia", CAN: "Canada", AUS: "Australia",
  KOR: "South Korea", MEX: "Mexico", IDN: "Indonesia",
  TUR: "Turkiye", SAU: "Saudi Arabia", ARG: "Argentina",
  ZAF: "South Africa", NGA: "Nigeria", EGY: "Egypt",
  ITA: "Italy", ESP: "Spain", NLD: "Netherlands", CHE: "Switzerland",
  SWE: "Sweden", NOR: "Norway", POL: "Poland", BEL: "Belgium",
  AUT: "Austria", THA: "Thailand", MYS: "Malaysia", SGP: "Singapore",
  PHL: "Philippines", VNM: "Vietnam", COL: "Colombia", CHL: "Chile",
  PER: "Peru", PAK: "Pakistan", BGD: "Bangladesh", KEN: "Kenya",
  GHA: "Ghana", ETH: "Ethiopia", TZA: "Tanzania", UGA: "Uganda",
  IRN: "Iran", IRQ: "Iraq", ISR: "Israel", ARE: "UAE",
  GRC: "Greece", PRT: "Portugal", IRL: "Ireland", DNK: "Denmark",
  FIN: "Finland", CZE: "Czechia", ROU: "Romania", HUN: "Hungary",
  UKR: "Ukraine", NZL: "New Zealand", HKG: "Hong Kong",
};

interface IMFResponse {
  values: Record<string, Record<string, Record<string, number>>>;
}

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
  return Object.entries(INDICATORS)
    .filter(
      ([id, v]) =>
        v.name.toLowerCase().includes(q) ||
        v.description.toLowerCase().includes(q) ||
        v.topics.some((t) => t.includes(q)) ||
        id.toLowerCase().includes(q)
    )
    .slice(0, limit)
    .map(([id, v]) => ({
      id,
      name: v.name,
      description: v.description,
      source: "IMF DataMapper",
      topics: v.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];

  let url = `${BASE}/${indicatorId}`;
  if (countries) {
    url += `/${countries}`;
  }

  const response = await fetchJSON<IMFResponse>(url);
  const indicatorData = response.values?.[indicatorId];

  if (!indicatorData) {
    return {
      name: indicator?.name ?? indicatorId,
      data: [],
    };
  }

  const data: DataPoint[] = [];

  for (const [countryCode, yearValues] of Object.entries(indicatorData)) {
    // Skip aggregate codes (typically longer than 3 chars or start with numbers)
    if (countryCode.length > 3) continue;

    const countryName =
      COUNTRY_NAMES[countryCode] ?? countryCode;

    for (const [yearStr, value] of Object.entries(yearValues)) {
      const year = parseInt(yearStr, 10);
      if (isNaN(year) || value === null || value === undefined) continue;

      data.push({
        country: countryCode,
        countryName,
        year,
        value,
      });
    }
  }

  data.sort((a, b) => a.year - b.year);

  return {
    name: indicator?.name ?? indicatorId,
    data,
  };
}

export function getSourceUrl(indicatorId: string): string {
  return `https://www.imf.org/external/datamapper/${indicatorId}`;
}
