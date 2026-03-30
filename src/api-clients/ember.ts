import type { DataPoint, IndicatorSearchResult } from "../types.js";

// Ember publishes bulk CSV data on Google Cloud Storage (no auth required).
// We parse the yearly long-format CSV which contains all datasets.
const YEARLY_CSV_URL =
  "https://storage.googleapis.com/emb-prod-bkt-publicdata/public-downloads/yearly_full_release_long_format.csv";

// Curated indicators mapped to (Category, Subcategory, Variable, Unit) tuples in the CSV.
const INDICATORS: Record<
  string,
  {
    name: string;
    category: string;
    subcategory: string;
    variable: string;
    unit: string;
    topics: string[];
  }
> = {
  // Generation by fuel (TWh)
  "GEN-COAL": {
    name: "Electricity generation from coal (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Coal",
    unit: "TWh",
    topics: ["energy", "electricity", "fossil", "coal"],
  },
  "GEN-GAS": {
    name: "Electricity generation from gas (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Gas",
    unit: "TWh",
    topics: ["energy", "electricity", "fossil", "gas"],
  },
  "GEN-SOLAR": {
    name: "Electricity generation from solar (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Solar",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable", "solar"],
  },
  "GEN-WIND": {
    name: "Electricity generation from wind (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Wind",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable", "wind"],
  },
  "GEN-HYDRO": {
    name: "Electricity generation from hydro (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Hydro",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable", "hydro"],
  },
  "GEN-NUCLEAR": {
    name: "Electricity generation from nuclear (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Nuclear",
    unit: "TWh",
    topics: ["energy", "electricity", "nuclear"],
  },
  "GEN-BIOENERGY": {
    name: "Electricity generation from bioenergy (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Bioenergy",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable", "bioenergy"],
  },
  "GEN-OTHER-FOSSIL": {
    name: "Electricity generation from other fossil (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Other Fossil",
    unit: "TWh",
    topics: ["energy", "electricity", "fossil"],
  },
  "GEN-OTHER-RENEW": {
    name: "Electricity generation from other renewables (TWh)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Other Renewables",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable"],
  },
  // Aggregate generation
  "GEN-TOTAL": {
    name: "Total electricity generation (TWh)",
    category: "Electricity generation",
    subcategory: "Total",
    variable: "Total Generation",
    unit: "TWh",
    topics: ["energy", "electricity"],
  },
  "GEN-CLEAN": {
    name: "Clean electricity generation (TWh)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Clean",
    unit: "TWh",
    topics: ["energy", "electricity", "clean"],
  },
  "GEN-FOSSIL": {
    name: "Fossil electricity generation (TWh)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Fossil",
    unit: "TWh",
    topics: ["energy", "electricity", "fossil"],
  },
  "GEN-RENEWABLES": {
    name: "Renewable electricity generation (TWh)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Renewables",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable"],
  },
  "GEN-WIND-SOLAR": {
    name: "Wind and solar generation (TWh)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Wind and Solar",
    unit: "TWh",
    topics: ["energy", "electricity", "renewable", "wind", "solar"],
  },
  // Generation shares (%)
  "SHARE-COAL": {
    name: "Coal share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Coal",
    unit: "%",
    topics: ["energy", "electricity", "fossil", "coal"],
  },
  "SHARE-GAS": {
    name: "Gas share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Gas",
    unit: "%",
    topics: ["energy", "electricity", "fossil", "gas"],
  },
  "SHARE-SOLAR": {
    name: "Solar share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Solar",
    unit: "%",
    topics: ["energy", "electricity", "renewable", "solar"],
  },
  "SHARE-WIND": {
    name: "Wind share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Fuel",
    variable: "Wind",
    unit: "%",
    topics: ["energy", "electricity", "renewable", "wind"],
  },
  "SHARE-RENEWABLES": {
    name: "Renewable share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Renewables",
    unit: "%",
    topics: ["energy", "electricity", "renewable"],
  },
  "SHARE-CLEAN": {
    name: "Clean share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Clean",
    unit: "%",
    topics: ["energy", "electricity", "clean"],
  },
  "SHARE-FOSSIL": {
    name: "Fossil share of electricity generation (%)",
    category: "Electricity generation",
    subcategory: "Aggregate fuel",
    variable: "Fossil",
    unit: "%",
    topics: ["energy", "electricity", "fossil"],
  },
  // Emissions
  "EMISSIONS-TOTAL": {
    name: "Power sector CO2 emissions (mtCO2)",
    category: "Power sector emissions",
    subcategory: "Total",
    variable: "Total emissions",
    unit: "mtCO2",
    topics: ["energy", "emissions", "climate"],
  },
  "EMISSIONS-INTENSITY": {
    name: "Carbon intensity of electricity (gCO2/kWh)",
    category: "Power sector emissions",
    subcategory: "CO2 intensity",
    variable: "CO2 intensity",
    unit: "gCO2/kWh",
    topics: ["energy", "emissions", "climate"],
  },
  // Demand
  "DEMAND-TOTAL": {
    name: "Electricity demand (TWh)",
    category: "Electricity demand",
    subcategory: "Demand",
    variable: "Demand",
    unit: "TWh",
    topics: ["energy", "electricity", "demand"],
  },
  "DEMAND-PER-CAPITA": {
    name: "Electricity demand per capita (MWh)",
    category: "Electricity demand",
    subcategory: "Demand per capita",
    variable: "Demand per capita",
    unit: "MWh",
    topics: ["energy", "electricity", "demand"],
  },
  // Capacity
  "CAP-SOLAR": {
    name: "Solar installed capacity (GW)",
    category: "Capacity",
    subcategory: "Fuel",
    variable: "Solar",
    unit: "GW",
    topics: ["energy", "renewable", "solar", "capacity"],
  },
  "CAP-WIND": {
    name: "Wind installed capacity (GW)",
    category: "Capacity",
    subcategory: "Fuel",
    variable: "Wind",
    unit: "GW",
    topics: ["energy", "renewable", "wind", "capacity"],
  },
  "CAP-CLEAN": {
    name: "Clean installed capacity (GW)",
    category: "Capacity",
    subcategory: "Aggregate fuel",
    variable: "Clean",
    unit: "GW",
    topics: ["energy", "clean", "capacity"],
  },
  "CAP-FOSSIL": {
    name: "Fossil installed capacity (GW)",
    category: "Capacity",
    subcategory: "Aggregate fuel",
    variable: "Fossil",
    unit: "GW",
    topics: ["energy", "fossil", "capacity"],
  },
  // Net imports
  "NET-IMPORTS": {
    name: "Net electricity imports (TWh)",
    category: "Electricity imports",
    subcategory: "Electricity imports",
    variable: "Net Imports",
    unit: "TWh",
    topics: ["energy", "electricity", "trade"],
  },
};

// CSV column indices (from the header row)
interface CsvRow {
  area: string;
  isoCode: string;
  year: string;
  areaType: string;
  category: string;
  subcategory: string;
  variable: string;
  unit: string;
  value: string;
}

// Cache the parsed CSV in memory for the lifetime of the process.
let cachedRows: CsvRow[] | null = null;

function parseCSVLine(line: string): string[] {
  const fields: string[] = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (inQuotes) {
      if (ch === '"' && line[i + 1] === '"') {
        current += '"';
        i++;
      } else if (ch === '"') {
        inQuotes = false;
      } else {
        current += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ",") {
        fields.push(current);
        current = "";
      } else {
        current += ch;
      }
    }
  }
  fields.push(current);
  return fields;
}

async function loadData(): Promise<CsvRow[]> {
  if (cachedRows) return cachedRows;

  console.log("Downloading Ember yearly data (~47 MB)...");
  const res = await fetch(YEARLY_CSV_URL);
  if (!res.ok) {
    throw new Error(`Ember CSV download failed: ${res.status} ${res.statusText}`);
  }
  const text = await res.text();
  const lines = text.split("\n");

  // Parse header to find column indices
  const header = parseCSVLine(lines[0]);
  const colMap: Record<string, number> = {};
  for (let i = 0; i < header.length; i++) {
    colMap[header[i].trim()] = i;
  }

  const areaIdx = colMap["Area"];
  const isoIdx = colMap["Country code"] ?? colMap["ISO 3 code"];
  const yearIdx = colMap["Year"];
  const areaTypeIdx = colMap["Area type"];
  const categoryIdx = colMap["Category"];
  const subcategoryIdx = colMap["Subcategory"];
  const variableIdx = colMap["Variable"];
  const unitIdx = colMap["Unit"];
  const valueIdx = colMap["Value"];

  if (valueIdx === undefined) {
    throw new Error(
      `Ember CSV has unexpected columns. Found: ${header.join(", ")}`
    );
  }

  const rows: CsvRow[] = [];
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    const fields = parseCSVLine(line);
    // Only include individual countries, not aggregate regions
    const areaType = fields[areaTypeIdx]?.trim() ?? "";
    if (areaType !== "Country" && areaType !== "Country or economy") continue;

    rows.push({
      area: fields[areaIdx]?.trim() ?? "",
      isoCode: fields[isoIdx]?.trim() ?? "",
      year: fields[yearIdx]?.trim() ?? "",
      areaType,
      category: fields[categoryIdx]?.trim() ?? "",
      subcategory: fields[subcategoryIdx]?.trim() ?? "",
      variable: fields[variableIdx]?.trim() ?? "",
      unit: fields[unitIdx]?.trim() ?? "",
      value: fields[valueIdx]?.trim() ?? "",
    });
  }

  cachedRows = rows;
  console.log(`Loaded ${rows.length} country-level data points from Ember.`);
  return rows;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  return Object.entries(INDICATORS)
    .filter(([id, ind]) => {
      const haystack =
        `${id} ${ind.name} ${ind.category} ${ind.variable} ${ind.topics.join(" ")}`.toLowerCase();
      return q.split(/\s+/).every((word) => haystack.includes(word));
    })
    .slice(0, limit)
    .map(([id, ind]) => ({
      id,
      name: ind.name,
      description: `Ember ${ind.category} - ${ind.variable} (${ind.unit})`,
      source: "Ember",
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
      `Unknown Ember indicator: ${indicatorId}. Use searchIndicators() to find valid IDs.`
    );
  }

  const rows = await loadData();

  const countryFilter = countries
    ? new Set(countries.split(",").map((c) => c.trim().toUpperCase()))
    : null;

  const data: DataPoint[] = [];
  for (const row of rows) {
    if (row.category !== indicator.category) continue;
    if (row.subcategory !== indicator.subcategory) continue;
    if (row.variable !== indicator.variable) continue;
    if (row.unit !== indicator.unit) continue;
    if (countryFilter && !countryFilter.has(row.isoCode)) continue;

    const value = parseFloat(row.value);
    if (isNaN(value)) continue;

    data.push({
      country: row.isoCode,
      countryName: row.area,
      year: parseInt(row.year, 10),
      value,
    });
  }

  data.sort((a, b) => a.year - b.year);
  return { name: indicator.name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return "https://ember-energy.org/data/yearly-electricity-data/";
}
