import type { DataPoint, IndicatorSearchResult } from "../types.js";

const BASE = "https://archive-api.open-meteo.com/v1/archive";

// Capital city coordinates for major countries
const CAPITALS: Record<string, { lat: number; lon: number; name: string }> = {
  USA: { lat: 38.9, lon: -77.0, name: "United States" },
  GBR: { lat: 51.5, lon: -0.1, name: "United Kingdom" },
  FRA: { lat: 48.9, lon: 2.3, name: "France" },
  DEU: { lat: 52.5, lon: 13.4, name: "Germany" },
  JPN: { lat: 35.7, lon: 139.7, name: "Japan" },
  CHN: { lat: 39.9, lon: 116.4, name: "China" },
  IND: { lat: 28.6, lon: 77.2, name: "India" },
  BRA: { lat: -15.8, lon: -47.9, name: "Brazil" },
  RUS: { lat: 55.8, lon: 37.6, name: "Russia" },
  AUS: { lat: -35.3, lon: 149.1, name: "Australia" },
  CAN: { lat: 45.4, lon: -75.7, name: "Canada" },
  MEX: { lat: 19.4, lon: -99.1, name: "Mexico" },
  ZAF: { lat: -25.7, lon: 28.2, name: "South Africa" },
  NGA: { lat: 9.1, lon: 7.5, name: "Nigeria" },
  EGY: { lat: 30.0, lon: 31.2, name: "Egypt" },
  KEN: { lat: -1.3, lon: 36.8, name: "Kenya" },
  KOR: { lat: 37.6, lon: 127.0, name: "South Korea" },
  IDN: { lat: -6.2, lon: 106.8, name: "Indonesia" },
  TUR: { lat: 39.9, lon: 32.9, name: "Turkey" },
  SAU: { lat: 24.7, lon: 46.7, name: "Saudi Arabia" },
  ARG: { lat: -34.6, lon: -58.4, name: "Argentina" },
  COL: { lat: 4.7, lon: -74.1, name: "Colombia" },
  THA: { lat: 13.8, lon: 100.5, name: "Thailand" },
  ITA: { lat: 41.9, lon: 12.5, name: "Italy" },
  ESP: { lat: 40.4, lon: -3.7, name: "Spain" },
  POL: { lat: 52.2, lon: 21.0, name: "Poland" },
  SWE: { lat: 59.3, lon: 18.1, name: "Sweden" },
  NOR: { lat: 59.9, lon: 10.8, name: "Norway" },
  FIN: { lat: 60.2, lon: 24.9, name: "Finland" },
  NLD: { lat: 52.4, lon: 4.9, name: "Netherlands" },
  CHE: { lat: 46.9, lon: 7.4, name: "Switzerland" },
  PER: { lat: -12.0, lon: -77.0, name: "Peru" },
  CHL: { lat: -33.4, lon: -70.7, name: "Chile" },
  PHL: { lat: 14.6, lon: 121.0, name: "Philippines" },
  VNM: { lat: 21.0, lon: 105.9, name: "Vietnam" },
  BGD: { lat: 23.8, lon: 90.4, name: "Bangladesh" },
  PAK: { lat: 33.7, lon: 73.1, name: "Pakistan" },
  ETH: { lat: 9.0, lon: 38.7, name: "Ethiopia" },
  TZA: { lat: -6.8, lon: 39.3, name: "Tanzania" },
  GHA: { lat: 5.6, lon: -0.2, name: "Ghana" },
  MAR: { lat: 34.0, lon: -6.8, name: "Morocco" },
  IRQ: { lat: 33.3, lon: 44.4, name: "Iraq" },
  IRN: { lat: 35.7, lon: 51.4, name: "Iran" },
  ISR: { lat: 31.8, lon: 35.2, name: "Israel" },
  JOR: { lat: 31.9, lon: 35.9, name: "Jordan" },
  UKR: { lat: 50.5, lon: 30.5, name: "Ukraine" },
  MYS: { lat: 3.1, lon: 101.7, name: "Malaysia" },
  SGP: { lat: 1.3, lon: 103.8, name: "Singapore" },
  NZL: { lat: -41.3, lon: 174.8, name: "New Zealand" },
  ARE: { lat: 24.5, lon: 54.4, name: "UAE" },
};

interface ClimateIndicator {
  name: string;
  description: string;
  variable: string;
  aggregation: "mean" | "max" | "min" | "sum";
  topics: string[];
}

const INDICATORS: Record<string, ClimateIndicator> = {
  "temperature_mean": {
    name: "Annual Mean Temperature",
    description: "Average daily mean temperature across the year in degrees Celsius",
    variable: "temperature_2m_mean",
    aggregation: "mean",
    topics: ["climate", "temperature", "environment"],
  },
  "temperature_max": {
    name: "Annual Maximum Temperature",
    description: "Average daily maximum temperature across the year in degrees Celsius",
    variable: "temperature_2m_max",
    aggregation: "mean",
    topics: ["climate", "temperature", "environment"],
  },
  "precipitation_total": {
    name: "Annual Total Precipitation",
    description: "Total annual precipitation in millimeters",
    variable: "precipitation_sum",
    aggregation: "sum",
    topics: ["climate", "precipitation", "environment", "water"],
  },
  "wind_speed_mean": {
    name: "Annual Mean Wind Speed",
    description: "Average daily maximum wind speed in km/h",
    variable: "wind_speed_10m_max",
    aggregation: "mean",
    topics: ["climate", "wind", "environment", "energy"],
  },
};

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Open-Meteo API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function searchIndicators(
  query: string,
  limit = 20
): Promise<IndicatorSearchResult[]> {
  const q = query.toLowerCase();
  return Object.entries(INDICATORS)
    .filter(([code, info]) =>
      code.includes(q) ||
      info.name.toLowerCase().includes(q) ||
      info.description.toLowerCase().includes(q) ||
      info.topics.some(t => t.includes(q))
    )
    .slice(0, limit)
    .map(([code, info]) => ({
      id: code,
      name: info.name,
      description: info.description,
      source: "Open-Meteo Historical Weather",
      topics: info.topics,
    }));
}

export async function fetchIndicatorData(
  indicatorId: string,
  countries?: string
): Promise<{ name: string; data: DataPoint[] }> {
  const indicator = INDICATORS[indicatorId];
  if (!indicator) {
    throw new Error(`Unknown Open-Meteo indicator: ${indicatorId}. Available: ${Object.keys(INDICATORS).join(", ")}`);
  }

  const countryFilter = countries?.split(",").map(c => c.trim().toUpperCase());
  const capitalsToFetch = countryFilter
    ? Object.entries(CAPITALS).filter(([code]) => countryFilter.includes(code))
    : Object.entries(CAPITALS);

  const data: DataPoint[] = [];

  // Fetch data for each capital city, year by year aggregated
  // Open-Meteo provides daily data; we aggregate to annual
  for (const [code, capital] of capitalsToFetch) {
    try {
      const url = `${BASE}?latitude=${capital.lat}&longitude=${capital.lon}&start_date=1960-01-01&end_date=2024-12-31&daily=${indicator.variable}&timezone=auto`;
      const response = await fetchJSON<{
        daily: { time: string[]; [key: string]: number[] | string[] };
      }>(url);

      const times = response.daily?.time as string[];
      const values = response.daily?.[indicator.variable] as number[];

      if (!times || !values) continue;

      // Aggregate by year
      const yearData: Record<number, number[]> = {};
      for (let i = 0; i < times.length; i++) {
        const year = parseInt(times[i].slice(0, 4), 10);
        const val = values[i];
        if (val === null || val === undefined || isNaN(val)) continue;
        if (!yearData[year]) yearData[year] = [];
        yearData[year].push(val);
      }

      for (const [yearStr, vals] of Object.entries(yearData)) {
        const year = parseInt(yearStr, 10);
        let value: number;
        if (indicator.aggregation === "sum") {
          value = vals.reduce((a, b) => a + b, 0);
        } else {
          value = vals.reduce((a, b) => a + b, 0) / vals.length;
        }
        data.push({
          country: code,
          countryName: capital.name,
          year,
          value: Math.round(value * 100) / 100,
        });
      }
    } catch {
      // Skip countries that fail
      continue;
    }
  }

  data.sort((a, b) => a.year - b.year);
  return { name: indicator.name, data };
}

export function getSourceUrl(indicatorId: string): string {
  return `https://open-meteo.com/en/docs/historical-weather-api`;
}
