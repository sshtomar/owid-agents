import React from "react";
import { COLORS, FONTS } from "../../theme";
import type { MetricKey } from "./types";
import { getScaleConfig, makeColorScale } from "./colorScales";

interface MapLegendProps {
  metric: MetricKey;
}

export default function MapLegend({ metric }: MapLegendProps) {
  const config = getScaleConfig(metric);
  const scale = makeColorScale(config.domain, config.colors);
  const steps = 40;
  const gradientStops: string[] = [];

  for (let i = 0; i <= steps; i++) {
    const value = config.domain[0] + (config.domain[1] - config.domain[0]) * (i / steps);
    gradientStops.push(scale(value));
  }

  const gradient = `linear-gradient(to right, ${gradientStops.join(", ")})`;

  return (
    <div style={{ marginTop: 8 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: 4,
          fontFamily: FONTS.mono,
          fontSize: 9,
          color: COLORS.textMuted,
        }}
      >
        <span>
          {config.domain[0]} {config.unit}
        </span>
        <span style={{ color: COLORS.textMid, fontWeight: 500 }}>
          {config.label}
        </span>
        <span>
          {config.domain[1]}+ {config.unit}
        </span>
      </div>
      <div
        style={{
          height: 8,
          borderRadius: 2,
          background: gradient,
        }}
      />
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          marginTop: 6,
          fontFamily: FONTS.mono,
          fontSize: 9,
          color: COLORS.textMuted,
        }}
      >
        <div
          style={{
            width: 12,
            height: 8,
            borderRadius: 1,
            backgroundColor: COLORS.inputBg,
            border: `1px solid ${COLORS.border}`,
          }}
        />
        <span>No data</span>
      </div>
    </div>
  );
}
