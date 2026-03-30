import { COLORS } from "../../theme";
import type { MetricKey } from "./types";

function hexToRgb(hex: string): [number, number, number] {
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}

function rgbToHex(r: number, g: number, b: number): string {
  return (
    "#" +
    ((1 << 24) | (Math.round(r) << 16) | (Math.round(g) << 8) | Math.round(b))
      .toString(16)
      .slice(1)
  );
}

function interpolateColor(
  c1: [number, number, number],
  c2: [number, number, number],
  t: number,
): string {
  return rgbToHex(
    c1[0] + (c2[0] - c1[0]) * t,
    c1[1] + (c2[1] - c1[1]) * t,
    c1[2] + (c2[2] - c1[2]) * t,
  );
}

export function makeColorScale(
  domain: [number, number],
  colors: string[],
): (value: number | null) => string {
  const rgbStops = colors.map(hexToRgb);
  const [min, max] = domain;

  return (value: number | null) => {
    if (value === null || value === undefined) return COLORS.inputBg;
    const t = Math.max(0, Math.min(1, (value - min) / (max - min)));
    const segment = t * (rgbStops.length - 1);
    const i = Math.min(Math.floor(segment), rgbStops.length - 2);
    const localT = segment - i;
    return interpolateColor(rgbStops[i], rgbStops[i + 1], localT);
  };
}

interface ScaleConfig {
  domain: [number, number];
  colors: string[];
  label: string;
  unit: string;
}

const SCALE_CONFIGS: Record<MetricKey, ScaleConfig> = {
  carbonIntensity: {
    domain: [0, 800],
    colors: ["#2D8B4E", "#F9C74F", "#D32F2F"],
    label: "Carbon Intensity",
    unit: "gCO2/kWh",
  },
  shareClean: {
    domain: [0, 100],
    colors: ["#D32F2F", "#F9C74F", "#2D8B4E"],
    label: "Clean Share",
    unit: "%",
  },
  shareFossil: {
    domain: [0, 100],
    colors: ["#2D8B4E", "#F9C74F", "#D32F2F"],
    label: "Fossil Share",
    unit: "%",
  },
  shareRenewables: {
    domain: [0, 100],
    colors: ["#E8E4D9", "#7BC47F", "#2D8B4E"],
    label: "Renewables",
    unit: "%",
  },
  demandPerCapita: {
    domain: [0, 25],
    colors: ["#E8E4D9", "#6BAED6", "#1A237E"],
    label: "Demand / Capita",
    unit: "MWh",
  },
  demandTotal: {
    domain: [0, 4000],
    colors: ["#E8E4D9", "#6BAED6", "#1A237E"],
    label: "Total Demand",
    unit: "TWh",
  },
  emissionsTotal: {
    domain: [0, 5000],
    colors: ["#E8E4D9", "#E57373", "#B71C1C"],
    label: "Emissions",
    unit: "mtCO2",
  },
  generationTotal: {
    domain: [0, 4000],
    colors: ["#E8E4D9", "#FFB74D", "#E65100"],
    label: "Generation",
    unit: "TWh",
  },
};

export function getScaleConfig(metric: MetricKey): ScaleConfig {
  return SCALE_CONFIGS[metric];
}

export function getColorScale(metric: MetricKey): (value: number | null) => string {
  const config = SCALE_CONFIGS[metric];
  return makeColorScale(config.domain, config.colors);
}
