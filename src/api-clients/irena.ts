import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://pxweb.irena.org/api/v1/en/IRENASTAT";

// PxWeb tables change names with each release (e.g. _2025_H2_PX.px).
// We discover the current table name dynamically from the folder listing.
const FOLDERS: Record<string, string> = {
  capacity: "Power Capacity and Generation",
  finance: "Finance",
  heat: "Heat Generation",
};

// Technology codes in the Country_ELECSTAT table (0-based positional indices).
const TECHNOLOGIES: Record<string, string> = {
  "0": "Total renewable",
  "1": "Solar photovoltaic",
  "2": "Solar thermal energy",
  "3": "Onshore wind energy",
  "4": "Offshore wind energy",
  "5": "Renewable hydropower",
  "6": "Mixed Hydro Plants",
  "7": "Marine energy",
  "8": "Solid biofuels",
  "9": "Renewable municipal waste",
  "10": "Liquid biofuels",
  "11": "Biogas",
  "12": "Geothermal energy",
  "13": "Total non-renewable",
  "14": "Pumped storage",
  "15": "Coal and peat",
  "16": "Oil",
  "17": "Natural gas",
  "18": "Fossil fuels n.e.s.",
  "19": "Nuclear",
  "20": "Other non-renewable energy",
};

// Curated indicators exposed for search/discovery.
// Each maps to a (technology, dataType) pair in the ELECSTAT table.
// dataType: "0" = Electricity capacity (MW), "1" = Electricity generation (GWh)
// Grid connection: "0" = All
const INDICATORS: Record<
  string,
  { name: string; tech: string; dataType: string; topics: string[] }
> = {
  // Generation (dataType "1")
  "ELEC-GEN-SOLAR-PV": {
    name: "Solar PV electricity generation (GWh)",
    tech: "1",
    dataType: "1",
    topics: ["energy", "renewable", "solar"],
  },
  "ELEC-GEN-WIND-ONSHORE": {
    name: "Onshore wind electricity generation (GWh)",
    tech: "3",
    dataType: "1",
    topics: ["energy", "renewable", "wind"],
  },
  "ELEC-GEN-WIND-OFFSHORE": {
    name: "Offshore wind electricity generation (GWh)",
    tech: "4",
    dataType: "1",
    topics: ["energy", "renewable", "wind"],
  },
  "ELEC-GEN-HYDRO": {
    name: "Hydropower electricity generation (GWh)",
    tech: "5",
    dataType: "1",
    topics: ["energy", "renewable", "hydro"],
  },
  "ELEC-GEN-GEOTHERMAL": {
    name: "Geothermal electricity generation (GWh)",
    tech: "12",
    dataType: "1",
    topics: ["energy", "renewable", "geothermal"],
  },
  "ELEC-GEN-BIOENERGY": {
    name: "Solid biofuels electricity generation (GWh)",
    tech: "8",
    dataType: "1",
    topics: ["energy", "renewable", "bioenergy"],
  },
  "ELEC-GEN-TOTAL-RENEW": {
    name: "Total renewable electricity generation (GWh)",
    tech: "0",
    dataType: "1",
    topics: ["energy", "renewable"],
  },
  "ELEC-GEN-NUCLEAR": {
    name: "Nuclear electricity generation (GWh)",
    tech: "19",
    dataType: "1",
    topics: ["energy", "nuclear"],
  },
  "ELEC-GEN-COAL": {
    name: "Coal and peat electricity generation (GWh)",
    tech: "15",
    dataType: "1",
    topics: ["energy", "fossil", "coal"],
  },
  "ELEC-GEN-GAS": {
    name: "Natural gas electricity generation (GWh)",
    tech: "17",
    dataType: "1",
    topics: ["energy", "fossil", "gas"],
  },
  "ELEC-GEN-OIL": {
    name: "Oil electricity generation (GWh)",
    tech: "16",
    dataType: "1",
    topics: ["energy", "fossil", "oil"],
  },
  "ELEC-GEN-TOTAL-NONRENEW": {
    name: "Total non-renewable electricity generation (GWh)",
    tech: "13",
    dataType: "1",
    topics: ["energy", "fossil"],
  },
  // Capacity (dataType "0")
  "ELEC-CAP-SOLAR-PV": {
    name: "Solar PV installed capacity (MW)",
    tech: "1",
    dataType: "0",
    topics: ["energy", "renewable", "solar", "capacity"],
  },
  "ELEC-CAP-WIND-ONSHORE": {
    name: "Onshore wind installed capacity (MW)",
    tech: "3",
    dataType: "0",
    topics: ["energy", "renewable", "wind", "capacity"],
  },
  "ELEC-CAP-WIND-OFFSHORE": {
    name: "Offshore wind installed capacity (MW)",
    tech: "4",
    dataType: "0",
    topics: ["energy", "renewable", "wind", "capacity"],
  },
  "ELEC-CAP-HYDRO": {
    name: "Hydropower installed capacity (MW)",
    tech: "5",
    dataType: "0",
    topics: ["energy", "renewable", "hydro", "capacity"],
  },
  "ELEC-CAP-GEOTHERMAL": {
    name: "Geothermal installed capacity (MW)",
    tech: "12",
    dataType: "0",
    topics: ["energy", "renewable", "geothermal", "capacity"],
  },
  "ELEC-CAP-TOTAL-RENEW": {
    name: "Total renewable installed capacity (MW)",
    tech: "0",
    dataType: "0",
    topics: ["energy", "renewable", "capacity"],
  },
  "ELEC-CAP-NUCLEAR": {
    name: "Nuclear installed capacity (MW)",
    tech: "19",
    dataType: "0",
    topics: ["energy", "nuclear", "capacity"],
  },
  "ELEC-CAP-TOTAL-NONRENEW": {
    name: "Total non-renewable installed capacity (MW)",
    tech: "13",
    dataType: "0",
    topics: ["energy", "fossil", "capacity"],
  },
};

interface PxWebFolder {
  id: string;
  type: "l" | "t"; // l = folder, t = table
  text: string;
}

interface PxWebColumn {
  code: string;
  text: string;
  type: string;
}

interface PxWebDataItem {
  key: string[];
  values: string[];
}

interface PxWebResponse {
  columns: PxWebColumn[];
  data: PxWebDataItem[];
}

async function fetchJSON<T>(url: string, body?: unknown): Promise<T> {
  const opts: RequestInit = body
    ? { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }
    : {};
  const res = await fetch(url, opts);
  if (!res.ok) {
    throw new Error(`IRENA API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

// Discover the current table file name in a given folder.
async function findTable(folder: string, prefix: string): Promise<string> {
  const items = await fetchJSON<PxWebFolder[]>(`${BASE}/${encodeURIComponent(folder)}`);
  const table = items.find((i) => i.type === "t" && i.id.startsWith(prefix));
  if (!table) {
    throw new Error(`No table matching "${prefix}" found in IRENA/${folder}`);
  }
  return table.id;
}

let cachedElecTable: string | null = null;

async function getElecTablePath(): Promise<string> {
  if (cachedElecTable) return cachedElecTable;
  const folder = FOLDERS.capacity;
  const tableId = await findTable(folder, "Country_ELECSTAT");
  cachedElecTable = `${BASE}/${encodeURIComponent(folder)}/${tableId}`;
  return cachedElecTable;
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
      description: `IRENA ${ind.dataType === "1" ? "capacity" : "generation"} data for ${TECHNOLOGIES[ind.tech] ?? "unknown"}`,
      source: "IRENA",
      topics: ind.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];
  if (!indicator) {
    throw new Error(`Unknown IRENA indicator: ${indicatorId}. Use searchIndicators() to find valid IDs.`);
  }

  const tablePath = await getElecTablePath();

  // Build PxWeb query. Omitting a dimension selects all values.
  // We filter by technology and data type, and optionally by country.
  const query: Array<{ code: string; selection: { filter: string; values: string[] } }> = [
    { code: "Technology", selection: { filter: "item", values: [indicator.tech] } },
    { code: "Data Type", selection: { filter: "item", values: [indicator.dataType] } },
    // Grid connection: "0" = All (on-grid + off-grid combined)
    { code: "Grid connection", selection: { filter: "item", values: ["0"] } },
  ];

  if (countries) {
    const codes = countries.split(",").map((c) => c.trim().toUpperCase());
    query.push({ code: "Country/area", selection: { filter: "item", values: codes } });
  }

  const response = await fetchJSON<PxWebResponse>(tablePath, {
    query,
    response: { format: "json" },
  });

  // PxWeb JSON format: columns array describes the key dimensions in order,
  // followed by a final column for the value. Each data row has key[] matching
  // the key columns, and values[] for the value column(s).
  // When we filter tech/dataType/grid to single values, the remaining key
  // dimensions are Country/area and Year.
  const keyColumns = response.columns.filter((c) => c.type !== "c");
  const countryKeyIdx = keyColumns.findIndex((c) => c.code === "Country/area");
  const yearKeyIdx = keyColumns.findIndex((c) => c.code === "Year");

  // Year index 0 = 2000, 1 = 2001, etc.
  const YEAR_BASE = 2000;

  const data: DataPoint[] = [];
  for (const row of response.data) {
    const rawValue = row.values[0];
    if (rawValue === ".." || rawValue === "") continue;
    const value = parseFloat(rawValue);
    if (isNaN(value)) continue;

    const countryCode = row.key[countryKeyIdx];
    const yearIndex = parseInt(row.key[yearKeyIdx], 10);
    const year = YEAR_BASE + yearIndex;

    data.push({
      country: countryCode,
      countryName: countryCode,
      year,
      value,
    });
  }

  data.sort((a, b) => a.year - b.year);
  return { name: indicator.name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return "https://pxweb.irena.org/pxweb/en/IRENASTAT/IRENASTAT__Power%20Capacity%20and%20Generation/";
}
