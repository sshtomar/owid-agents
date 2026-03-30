import React from "react";
import { COLORS, FONTS } from "../../theme";
import type { MetricKey } from "./types";

interface MetricOption {
  key: MetricKey;
  label: string;
  unit: string;
}

const METRICS: MetricOption[] = [
  { key: "carbonIntensity", label: "Carbon Intensity", unit: "gCO2/kWh" },
  { key: "shareClean", label: "Clean Energy", unit: "%" },
  { key: "shareFossil", label: "Fossil Fuels", unit: "%" },
  { key: "shareRenewables", label: "Renewables", unit: "%" },
  { key: "demandPerCapita", label: "Demand / Capita", unit: "MWh" },
  { key: "emissionsTotal", label: "CO2 Emissions", unit: "mtCO2" },
];

interface MetricSelectorProps {
  selected: MetricKey;
  onChange: (metric: MetricKey) => void;
}

export default function MetricSelector({
  selected,
  onChange,
}: MetricSelectorProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
      {METRICS.map((m) => {
        const isActive = m.key === selected;
        return (
          <button
            key={m.key}
            onClick={() => onChange(m.key)}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "8px 12px",
              borderRadius: 2,
              border: "none",
              backgroundColor: isActive ? COLORS.accent : "transparent",
              color: isActive ? COLORS.white : COLORS.text,
              cursor: "pointer",
              fontFamily: FONTS.mono,
              fontSize: 10,
              fontWeight: 500,
              letterSpacing: "0.3px",
              textAlign: "left",
              transition: "background-color 0.15s ease",
            }}
          >
            <span>{m.label}</span>
            <span
              style={{
                color: isActive ? "rgba(255,255,255,0.7)" : COLORS.textMuted,
                fontSize: 9,
              }}
            >
              {m.unit}
            </span>
          </button>
        );
      })}
    </div>
  );
}
