import React from "react";
import { motion } from "framer-motion";
import { COLORS, FONTS, SPRING } from "../../theme";
import type { CountryElectricity, FuelType } from "./types";
import { FUEL_COLORS, FUEL_LABELS, FUEL_ORDER } from "./types";

interface CountryPanelProps {
  country: CountryElectricity;
  year: number;
  onClose: () => void;
}

function StatBlock({
  label,
  value,
  unit,
}: {
  label: string;
  value: number | null;
  unit: string;
}) {
  return (
    <div style={{ flex: 1, minWidth: 80 }}>
      <div
        style={{
          fontSize: 9,
          textTransform: "uppercase",
          letterSpacing: "0.5px",
          color: COLORS.textMuted,
          fontFamily: FONTS.mono,
          marginBottom: 4,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 20,
          fontWeight: 700,
          color: COLORS.text,
          lineHeight: 1.1,
        }}
      >
        {value !== null ? formatValue(value) : "--"}
      </div>
      <div
        style={{
          fontSize: 9,
          color: COLORS.textMuted,
          fontFamily: FONTS.mono,
        }}
      >
        {unit}
      </div>
    </div>
  );
}

function formatValue(v: number): string {
  if (Math.abs(v) >= 1000) return v.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  if (Math.abs(v) >= 100) return v.toFixed(0);
  if (Math.abs(v) >= 10) return v.toFixed(1);
  return v.toFixed(2);
}

function GenerationMixBar({ country }: { country: CountryElectricity }) {
  const mix = country.generationMix;
  const total = FUEL_ORDER.reduce(
    (sum, fuel) => sum + (mix[fuel] ?? 0),
    0,
  );

  if (total <= 0) {
    return (
      <div
        style={{
          fontSize: 11,
          color: COLORS.textMuted,
          fontStyle: "italic",
        }}
      >
        No generation data available
      </div>
    );
  }

  const segments = FUEL_ORDER
    .map((fuel) => ({
      fuel,
      value: mix[fuel] ?? 0,
      pct: ((mix[fuel] ?? 0) / total) * 100,
    }))
    .filter((s) => s.pct > 0);

  return (
    <div>
      {/* Stacked bar */}
      <div
        style={{
          display: "flex",
          height: 24,
          borderRadius: 2,
          overflow: "hidden",
          marginBottom: 8,
        }}
      >
        {segments.map((s) => (
          <div
            key={s.fuel}
            style={{
              width: `${s.pct}%`,
              backgroundColor: FUEL_COLORS[s.fuel as FuelType],
              transition: "width 0.3s ease",
              minWidth: s.pct > 0 ? 2 : 0,
            }}
            title={`${FUEL_LABELS[s.fuel as FuelType]}: ${s.value.toFixed(1)} TWh (${s.pct.toFixed(1)}%)`}
          />
        ))}
      </div>
      {/* Legend */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "4px 12px",
        }}
      >
        {segments.map((s) => (
          <div
            key={s.fuel}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 4,
              fontSize: 10,
              fontFamily: FONTS.mono,
              color: COLORS.textMid,
            }}
          >
            <div
              style={{
                width: 8,
                height: 8,
                borderRadius: 1,
                backgroundColor: FUEL_COLORS[s.fuel as FuelType],
                flexShrink: 0,
              }}
            />
            <span>{FUEL_LABELS[s.fuel as FuelType]}</span>
            <span style={{ color: COLORS.textMuted }}>
              {s.pct.toFixed(0)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export function CountryPanelContent({
  country,
  year,
  onClose,
}: CountryPanelProps) {
  return (
    <div>
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          marginBottom: 20,
        }}
      >
        <div>
          <h2
            style={{
              fontSize: 18,
              fontWeight: 700,
              color: COLORS.text,
              margin: "0 0 4px",
              lineHeight: 1.2,
            }}
          >
            {country.countryName}
          </h2>
          <span
            style={{
              fontFamily: FONTS.mono,
              fontSize: 10,
              color: COLORS.textMuted,
              letterSpacing: "0.3px",
            }}
          >
            {country.countryCode} / {year}
          </span>
        </div>
        <button
          onClick={onClose}
          style={{
            border: "none",
            background: "none",
            cursor: "pointer",
            fontSize: 18,
            color: COLORS.textMuted,
            padding: "0 4px",
            lineHeight: 1,
          }}
          title="Close"
        >
          x
        </button>
      </div>

      {/* Key stats */}
      <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
        <StatBlock
          label="Carbon Intensity"
          value={country.carbonIntensity}
          unit="gCO2/kWh"
        />
        <StatBlock
          label="Clean Share"
          value={country.shareClean}
          unit="%"
        />
        <StatBlock
          label="Demand"
          value={country.demandTotal}
          unit="TWh"
        />
      </div>

      {/* More stats */}
      <div style={{ display: "flex", gap: 8, marginBottom: 24, flexWrap: "wrap" }}>
        <StatBlock
          label="Renewables"
          value={country.shareRenewables}
          unit="%"
        />
        <StatBlock
          label="Fossil"
          value={country.shareFossil}
          unit="%"
        />
        <StatBlock
          label="Emissions"
          value={country.emissionsTotal}
          unit="mtCO2"
        />
      </div>

      {/* Generation mix */}
      <div style={{ marginBottom: 20 }}>
        <div
          style={{
            fontSize: 9,
            textTransform: "uppercase",
            letterSpacing: "0.5px",
            color: COLORS.textMuted,
            fontFamily: FONTS.mono,
            marginBottom: 10,
          }}
        >
          Generation Mix
          {country.generationTotal !== null && (
            <span style={{ color: COLORS.textMid, marginLeft: 8 }}>
              {formatValue(country.generationTotal)} TWh total
            </span>
          )}
        </div>
        <GenerationMixBar country={country} />
      </div>

      {/* Provenance */}
      <div
        style={{
          marginTop: 24,
          paddingTop: 16,
          borderTop: `1px solid ${COLORS.border}`,
          fontSize: 10,
          color: COLORS.textMuted,
          lineHeight: 1.6,
        }}
      >
        <div
          style={{
            fontFamily: FONTS.mono,
            fontSize: 9,
            textTransform: "uppercase",
            letterSpacing: "0.5px",
            marginBottom: 6,
          }}
        >
          Data provenance
        </div>
        Discovered by agent from{" "}
        <a
          href="https://ember-energy.org/data/yearly-electricity-data/"
          target="_blank"
          rel="noopener noreferrer"
          style={{ color: COLORS.accent, textDecoration: "none" }}
        >
          Ember Yearly Electricity Data
        </a>
        . No manual scrapers -- agents search, validate, and catalog
        open datasets autonomously.
      </div>
    </div>
  );
}

export default function CountryPanel(props: CountryPanelProps) {
  return (
    <motion.div
      initial={{ x: 360, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      exit={{ x: 360, opacity: 0 }}
      transition={SPRING.slide}
      style={{
        width: 340,
        backgroundColor: COLORS.bg,
        borderLeft: `1px solid ${COLORS.borderStrong}`,
        padding: "20px 24px",
        overflowY: "auto",
        height: "100%",
        flexShrink: 0,
      }}
    >
      <CountryPanelContent {...props} />
    </motion.div>
  );
}
