export interface CountryElectricity {
  countryName: string;
  countryCode: string;
  carbonIntensity: number | null;
  shareClean: number | null;
  shareFossil: number | null;
  shareRenewables: number | null;
  demandTotal: number | null;
  demandPerCapita: number | null;
  emissionsTotal: number | null;
  generationTotal: number | null;
  generationMix: {
    coal: number | null;
    gas: number | null;
    nuclear: number | null;
    hydro: number | null;
    wind: number | null;
    solar: number | null;
    bioenergy: number | null;
  };
}

export interface MetricInfo {
  key: MetricKey;
  label: string;
  unit: string;
}

export type MetricKey =
  | "carbonIntensity"
  | "shareClean"
  | "shareFossil"
  | "shareRenewables"
  | "demandPerCapita"
  | "demandTotal"
  | "emissionsTotal"
  | "generationTotal";

export interface ElectricityMapResponse {
  availableYears: number[];
  availableMetrics: MetricInfo[];
  data: Record<number, Record<string, CountryElectricity>>;
}

export type FuelType = keyof CountryElectricity["generationMix"];

export const FUEL_COLORS: Record<FuelType, string> = {
  coal: "#545454",
  gas: "#C08040",
  nuclear: "#B07CC6",
  hydro: "#4682B4",
  wind: "#87CEEB",
  solar: "#E8B618",
  bioenergy: "#228B22",
};

export const FUEL_LABELS: Record<FuelType, string> = {
  coal: "Coal",
  gas: "Gas",
  nuclear: "Nuclear",
  hydro: "Hydro",
  wind: "Wind",
  solar: "Solar",
  bioenergy: "Bio",
};

export const FUEL_ORDER: FuelType[] = [
  "coal",
  "gas",
  "nuclear",
  "hydro",
  "wind",
  "solar",
  "bioenergy",
];
