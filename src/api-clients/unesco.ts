import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://api.uis.unesco.org/api/public/data/indicators";

// Curated catalog of interesting UNESCO indicators
const INDICATORS: Record<
  string,
  { name: string; description: string; topics: string[] }
> = {
  "XGDP.FSGOV": {
    name: "Government Education Spending (% of GDP)",
    description:
      "Total government expenditure on education as a percentage of GDP",
    topics: ["education", "spending", "government"],
  },
  "XUNIT.FSGOV.L02": {
    name: "Per-Pupil Government Spending, Primary (US$)",
    description:
      "Government expenditure per student in primary education, in current US dollars",
    topics: ["education", "spending", "primary"],
  },
  "NERT.1": {
    name: "Net Enrollment Rate, Primary (%)",
    description:
      "Total net enrollment rate in primary education, both sexes",
    topics: ["education", "enrollment", "primary"],
  },
  "NERA.2_3": {
    name: "Net Enrollment Rate, Secondary (%)",
    description:
      "Net enrollment rate in secondary education (lower and upper), both sexes",
    topics: ["education", "enrollment", "secondary"],
  },
  "GER.5T8": {
    name: "Gross Enrollment Ratio, Tertiary (%)",
    description:
      "Gross enrollment ratio in tertiary education, both sexes",
    topics: ["education", "enrollment", "tertiary", "university"],
  },
  "LR.AG15T99": {
    name: "Adult Literacy Rate (% ages 15+)",
    description:
      "Literacy rate among the population aged 15 years and older",
    topics: ["education", "literacy"],
  },
  "PTRHC.2_3": {
    name: "Pupil-Teacher Ratio, Secondary",
    description:
      "Number of students per teacher in secondary education",
    topics: ["education", "teachers", "quality"],
  },
  "ROFST.1.CP": {
    name: "Out-of-School Rate, Primary (%)",
    description:
      "Rate of children of primary school age who are not enrolled in school",
    topics: ["education", "out-of-school", "children"],
  },
  "GER.1": {
    name: "Gross Enrollment Ratio, Primary (%)",
    description:
      "Gross enrollment ratio in primary education, both sexes, as percentage of the relevant age group",
    topics: ["education", "enrollment", "primary"],
  },
  "GER.2": {
    name: "Gross Enrollment Ratio, Secondary (%)",
    description:
      "Gross enrollment ratio in secondary education, both sexes, as percentage of the relevant age group",
    topics: ["education", "enrollment", "secondary"],
  },
  "CR.1": {
    name: "Primary Completion Rate (%)",
    description:
      "Percentage of children who complete the last grade of primary education",
    topics: ["education", "completion", "primary"],
  },
};

// ISO3 code to name for common countries
const COUNTRY_NAMES: Record<string, string> = {
  USA: "United States", GBR: "United Kingdom", DEU: "Germany",
  FRA: "France", JPN: "Japan", CHN: "China", IND: "India",
  BRA: "Brazil", RUS: "Russia", CAN: "Canada", AUS: "Australia",
  KOR: "South Korea", MEX: "Mexico", IDN: "Indonesia",
  TUR: "Turkiye", ARG: "Argentina", ZAF: "South Africa",
  NGA: "Nigeria", EGY: "Egypt", ITA: "Italy", ESP: "Spain",
  NLD: "Netherlands", SWE: "Sweden", NOR: "Norway", POL: "Poland",
  THA: "Thailand", MYS: "Malaysia", SGP: "Singapore",
  PHL: "Philippines", VNM: "Vietnam", COL: "Colombia",
  CHL: "Chile", PER: "Peru", PAK: "Pakistan", BGD: "Bangladesh",
  KEN: "Kenya", GHA: "Ghana", ETH: "Ethiopia", TZA: "Tanzania",
  IRN: "Iran", ISR: "Israel", GRC: "Greece", PRT: "Portugal",
  IRL: "Ireland", DNK: "Denmark", FIN: "Finland", CZE: "Czechia",
  ROU: "Romania", HUN: "Hungary", UKR: "Ukraine", NZL: "New Zealand",
  MAR: "Morocco", DZA: "Algeria", TUN: "Tunisia", SEN: "Senegal",
  CMR: "Cameroon", CIV: "Cote d'Ivoire", MOZ: "Mozambique",
  MDG: "Madagascar", NPL: "Nepal", MMR: "Myanmar", KHM: "Cambodia",
  LKA: "Sri Lanka", JOR: "Jordan", LBN: "Lebanon",
};

interface UNESCORecord {
  indicatorId: string;
  geoUnit: string;
  year: number;
  value: number | null;
}

interface UNESCOResponse {
  records: UNESCORecord[];
}

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`UNESCO API error: ${res.status} ${res.statusText}`);
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
      source: "UNESCO Institute for Statistics",
      topics: v.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];

  let url = `${BASE}?indicator=${indicatorId}&start=1990&end=2024`;
  if (countries) {
    url += `&country=${countries}`;
  }

  const response = await fetchJSON<UNESCOResponse>(url);

  const name =
    indicator?.name ?? `UNESCO ${indicatorId}`;

  const data: DataPoint[] = response.records
    .filter((r) => r.value !== null && r.geoUnit && r.geoUnit.length <= 3)
    .map((r) => ({
      country: r.geoUnit,
      countryName: COUNTRY_NAMES[r.geoUnit] ?? r.geoUnit,
      year: r.year,
      value: r.value,
    }))
    .sort((a, b) => a.year - b.year);

  return { name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return "https://data.uis.unesco.org/";
}
