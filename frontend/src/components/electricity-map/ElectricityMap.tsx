import React, { useState, useCallback, useEffect, useRef, useMemo } from "react";
import { motion } from "framer-motion";
import { useApi } from "../../hooks/useApi";
import { useIsMobile } from "../../hooks/useIsMobile";
import WorldMap from "./WorldMap";
import YearSlider from "./YearSlider";
import MapLegend from "./MapLegend";
import { getColorScale } from "./colorScales";
import type {
  ElectricityMapResponse,
  MetricKey,
  CountryElectricity,
  FuelType,
} from "./types";
import { FUEL_COLORS, FUEL_LABELS, FUEL_ORDER } from "./types";

// -- Design tokens (VoltMetric style) --

const VM = {
  bg: "#F5F3EE",
  text: "#1A1A1A",
  textMuted: "#8A8A85",
  textMid: "#5C5C58",
  border: "#D8D5CC",
  borderLight: "#E8E6DF",
  accent: "#1A1A1A",
  white: "#FFFFFF",
  serif: "'Playfair Display', Georgia, 'Times New Roman', serif",
  sans: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
  mono: "'JetBrains Mono', 'SF Mono', monospace",
} as const;

type TabKey = "dashboard" | "generation" | "map" | "agents";

const TABS: { key: TabKey; label: string }[] = [
  { key: "dashboard", label: "Global Dashboard" },
  { key: "generation", label: "Generation Mix" },
  { key: "map", label: "Map View" },
  { key: "agents", label: "Discovery Logs" },
];

// -- Agent simulation data --

interface AgentInfo {
  name: string;
  status: "Live" | "Parsing" | "Idle" | "Syncing";
  message: string;
}

function getAgents(countryCount: number): AgentInfo[] {
  return [
    {
      name: "Agent-EMBER-01",
      status: "Live",
      message: `Streaming yearly CSV. ${countryCount} countries indexed.`,
    },
    {
      name: "Agent-IRENA-07",
      status: "Parsing",
      message: "PxWeb capacity tables. Schema mapping in progress.",
    },
    {
      name: "Agent-EIA-03",
      status: "Idle",
      message: "Wait cycle for EIA monthly reporting updates.",
    },
  ];
}

// -- Helpers --

function fmt(v: number | null, decimals = 1): string {
  if (v === null) return "--";
  if (Math.abs(v) >= 10000) return (v / 1000).toFixed(0) + "k";
  if (Math.abs(v) >= 1000)
    return v.toFixed(0).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  if (Math.abs(v) >= 100) return v.toFixed(0);
  return v.toFixed(decimals);
}

function fmtSub(v: number): string {
  return v.toFixed(1).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// -- Sub-components --

function StatusBadge({ status }: { status: AgentInfo["status"] }) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 8px",
        border: `1px solid ${VM.border}`,
        borderRadius: 2,
        fontSize: 9,
        fontFamily: VM.mono,
        fontWeight: 500,
        letterSpacing: "0.3px",
        color: status === "Live" ? VM.text : VM.textMuted,
        backgroundColor: status === "Live" ? VM.borderLight : "transparent",
      }}
    >
      {status}
    </span>
  );
}

function StatCard({
  label,
  value,
  unit,
  subtitle,
}: {
  label: string;
  value: string;
  unit: string;
  subtitle: string;
}) {
  return (
    <div
      style={{
        border: `1px solid ${VM.border}`,
        padding: "24px 28px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        minHeight: 150,
      }}
    >
      <div
        style={{
          fontSize: 10,
          fontFamily: VM.mono,
          fontWeight: 500,
          textTransform: "uppercase",
          letterSpacing: "1px",
          color: VM.textMuted,
          marginBottom: 12,
        }}
      >
        {label}
      </div>
      <div>
        <div
          style={{
            fontFamily: VM.serif,
            fontSize: 36,
            fontWeight: 400,
            color: VM.text,
            lineHeight: 1.1,
            letterSpacing: "-0.5px",
            marginBottom: 4,
          }}
        >
          {value}{" "}
          <span
            style={{ fontSize: 18, color: VM.textMid }}
            dangerouslySetInnerHTML={{ __html: unit }}
          />
        </div>
        <div
          style={{
            fontSize: 12,
            color: VM.textMuted,
            lineHeight: 1.4,
            marginTop: 8,
          }}
        >
          {subtitle}
        </div>
      </div>
    </div>
  );
}

function GenerationBar({ country }: { country: CountryElectricity }) {
  const total = FUEL_ORDER.reduce(
    (sum, f) => sum + (country.generationMix[f] ?? 0),
    0,
  );
  if (total <= 0) return null;

  const segments = FUEL_ORDER.map((fuel) => ({
    fuel,
    value: country.generationMix[fuel] ?? 0,
    pct: ((country.generationMix[fuel] ?? 0) / total) * 100,
  })).filter((s) => s.pct > 0.5);

  return (
    <div>
      <div
        style={{
          display: "flex",
          height: 32,
          overflow: "hidden",
          marginBottom: 12,
        }}
      >
        {segments.map((s) => (
          <div
            key={s.fuel}
            style={{
              width: `${s.pct}%`,
              backgroundColor: FUEL_COLORS[s.fuel as FuelType],
              transition: "width 0.4s ease",
              minWidth: 3,
              position: "relative",
            }}
            title={`${FUEL_LABELS[s.fuel as FuelType]}: ${fmtSub(s.value)} TWh`}
          />
        ))}
      </div>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "6px 16px",
        }}
      >
        {segments.map((s) => (
          <div
            key={s.fuel}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 6,
              fontSize: 11,
              color: VM.textMid,
            }}
          >
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: 1,
                backgroundColor: FUEL_COLORS[s.fuel as FuelType],
                flexShrink: 0,
              }}
            />
            <span style={{ fontWeight: 500 }}>
              {FUEL_LABELS[s.fuel as FuelType]}
            </span>
            <span
              style={{
                fontFamily: VM.mono,
                fontSize: 10,
                color: VM.textMuted,
              }}
            >
              {s.pct.toFixed(0)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// -- Main page --

export default function ElectricityMap() {
  const mobile = useIsMobile();
  const { data, loading, error } =
    useApi<ElectricityMapResponse>("/electricity-map");

  const [activeTab, setActiveTab] = useState<TabKey>("dashboard");
  const [selectedYear, setSelectedYear] = useState(2024);
  const [selectedMetric, setSelectedMetric] =
    useState<MetricKey>("carbonIntensity");
  const [selectedCountry, setSelectedCountry] = useState<string | null>(null);
  const [hoveredCountry, setHoveredCountry] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const playIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (data && data.availableYears.length > 0) {
      setSelectedYear(data.availableYears[data.availableYears.length - 1]);
    }
  }, [data]);

  useEffect(() => {
    if (!isPlaying || !data) return;
    const years = data.availableYears;
    playIntervalRef.current = setInterval(() => {
      setSelectedYear((prev) => {
        const idx = years.indexOf(prev);
        if (idx < 0 || idx >= years.length - 1) return years[0];
        return years[idx + 1];
      });
    }, 600);
    return () => {
      if (playIntervalRef.current) clearInterval(playIntervalRef.current);
    };
  }, [isPlaying, data]);

  const handlePlayToggle = useCallback(() => setIsPlaying((p) => !p), []);

  const colorScale = useMemo(
    () => getColorScale(selectedMetric),
    [selectedMetric],
  );

  const yearData = data?.data[selectedYear] ?? {};

  // Find the "selected" or default country for dashboard display
  const dashboardCountry: CountryElectricity | null = selectedCountry
    ? yearData[selectedCountry] ?? null
    : null;

  // Global aggregates
  const globalStats = useMemo(() => {
    const countries = Object.values(yearData);
    if (countries.length === 0) return null;

    const totalGen =
      countries.reduce((s, c) => s + (c.generationTotal ?? 0), 0);
    const totalDemand =
      countries.reduce((s, c) => s + (c.demandTotal ?? 0), 0);
    const totalEmissions =
      countries.reduce((s, c) => s + (c.emissionsTotal ?? 0), 0);

    // Weighted carbon intensity
    const ciWeighted =
      totalGen > 0
        ? countries.reduce(
            (s, c) =>
              s +
              (c.carbonIntensity ?? 0) * (c.generationTotal ?? 0),
            0,
          ) / totalGen
        : null;

    // Clean + renewable shares (weighted by generation)
    const cleanShare =
      totalGen > 0
        ? countries.reduce(
            (s, c) =>
              s + ((c.shareClean ?? 0) / 100) * (c.generationTotal ?? 0),
            0,
          ) /
          totalGen *
          100
        : null;

    const renewShare =
      totalGen > 0
        ? countries.reduce(
            (s, c) =>
              s +
              ((c.shareRenewables ?? 0) / 100) * (c.generationTotal ?? 0),
            0,
          ) /
          totalGen *
          100
        : null;

    // Top generation mix globally
    const globalMix: Record<FuelType, number> = {
      coal: 0, gas: 0, nuclear: 0, hydro: 0, wind: 0, solar: 0, bioenergy: 0,
    };
    for (const c of countries) {
      for (const fuel of FUEL_ORDER) {
        globalMix[fuel] += c.generationMix[fuel] ?? 0;
      }
    }

    // Top by generation
    const sorted = [...countries]
      .filter((c) => c.generationTotal !== null)
      .sort((a, b) => (b.generationTotal ?? 0) - (a.generationTotal ?? 0));

    return {
      totalGen,
      totalDemand,
      totalEmissions,
      ciWeighted,
      cleanShare,
      renewShare,
      globalMix,
      countryCount: countries.length,
      top5: sorted.slice(0, 5),
    };
  }, [yearData]);

  const agents = useMemo(
    () => getAgents(Object.keys(yearData).length),
    [yearData],
  );

  // Loading
  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          fontFamily: VM.mono,
          fontSize: 11,
          color: VM.textMuted,
          backgroundColor: VM.bg,
        }}
      >
        Loading electricity data...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          fontFamily: VM.mono,
          fontSize: 11,
          color: "#D32F2F",
          backgroundColor: VM.bg,
        }}
      >
        Failed to load: {error}
      </div>
    );
  }

  const minYear = data.availableYears[0];
  const maxYear = data.availableYears[data.availableYears.length - 1];

  // Display country (for dashboard)
  const display = dashboardCountry ?? (globalStats ? {
    countryName: "Global",
    countryCode: "WORLD",
    carbonIntensity: globalStats.ciWeighted,
    shareClean: globalStats.cleanShare,
    shareFossil: null,
    shareRenewables: globalStats.renewShare,
    demandTotal: globalStats.totalDemand,
    demandPerCapita: null,
    emissionsTotal: globalStats.totalEmissions,
    generationTotal: globalStats.totalGen,
    generationMix: globalStats.globalMix as CountryElectricity["generationMix"],
  } as CountryElectricity : null);

  const displayLabel = dashboardCountry
    ? dashboardCountry.countryName
    : "Global Overview";

  const displaySubtitle = dashboardCountry
    ? `Electricity data for ${dashboardCountry.countryName}, ${selectedYear}.`
    : `Aggregated grid metrics across ${globalStats?.countryCount ?? 0} countries.`;

  return (
    <div
      style={{
        backgroundColor: VM.bg,
        color: VM.text,
        fontFamily: VM.sans,
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {/* ---- Top nav ---- */}
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: mobile ? "14px 16px" : "14px 40px",
          borderBottom: `1px solid ${VM.border}`,
          flexShrink: 0,
        }}
      >
        <div
          style={{
            fontFamily: VM.serif,
            fontSize: 18,
            fontWeight: 600,
            color: VM.text,
            letterSpacing: "-0.3px",
            cursor: "pointer",
          }}
          onClick={() => {
            setSelectedCountry(null);
            setActiveTab("dashboard");
          }}
        >
          VoltMetric
        </div>

        {!mobile && (
          <nav
            style={{
              display: "flex",
              gap: 4,
            }}
          >
            {TABS.map((tab) => {
              const isActive = tab.key === activeTab;
              return (
                <button
                  key={tab.key}
                  onClick={() => setActiveTab(tab.key)}
                  style={{
                    padding: "7px 18px",
                    borderRadius: 20,
                    border: isActive
                      ? `1px solid ${VM.accent}`
                      : `1px solid ${VM.border}`,
                    backgroundColor: isActive ? VM.accent : "transparent",
                    color: isActive ? VM.white : VM.text,
                    fontFamily: VM.sans,
                    fontSize: 12,
                    fontWeight: 500,
                    cursor: "pointer",
                    transition: "all 0.15s ease",
                  }}
                >
                  {tab.label}
                </button>
              );
            })}
          </nav>
        )}

        <div style={{ display: "flex", gap: 6 }}>
          <button
            style={{
              padding: "7px 16px",
              border: `1px solid ${VM.border}`,
              borderRadius: 20,
              backgroundColor: "transparent",
              color: VM.text,
              fontFamily: VM.sans,
              fontSize: 12,
              fontWeight: 500,
              cursor: "pointer",
            }}
          >
            Export Data
          </button>
          {!mobile && (
            <button
              style={{
                padding: "7px 16px",
                border: `1px solid ${VM.border}`,
                borderRadius: 20,
                backgroundColor: "transparent",
                color: VM.text,
                fontFamily: VM.sans,
                fontSize: 12,
                fontWeight: 500,
                cursor: "pointer",
              }}
            >
              Settings
            </button>
          )}
        </div>
      </header>

      {/* Mobile tab bar */}
      {mobile && (
        <div
          style={{
            display: "flex",
            gap: 4,
            padding: "10px 16px",
            overflowX: "auto",
            borderBottom: `1px solid ${VM.borderLight}`,
          }}
        >
          {TABS.map((tab) => {
            const isActive = tab.key === activeTab;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                style={{
                  padding: "6px 14px",
                  borderRadius: 16,
                  border: isActive
                    ? `1px solid ${VM.accent}`
                    : `1px solid ${VM.border}`,
                  backgroundColor: isActive ? VM.accent : "transparent",
                  color: isActive ? VM.white : VM.text,
                  fontFamily: VM.sans,
                  fontSize: 11,
                  fontWeight: 500,
                  cursor: "pointer",
                  whiteSpace: "nowrap",
                  flexShrink: 0,
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>
      )}

      {/* ---- Content ---- */}
      <div style={{ flex: 1, overflow: "auto" }}>
        {/* Dashboard + Generation tabs share the main layout */}
        {(activeTab === "dashboard" || activeTab === "generation") && display && (
          <DashboardView
            display={display}
            displayLabel={displayLabel}
            displaySubtitle={displaySubtitle}
            selectedYear={selectedYear}
            availableYears={data.availableYears}
            onYearChange={setSelectedYear}
            agents={agents}
            globalStats={globalStats}
            activeTab={activeTab}
            mobile={mobile}
            onCountryClick={(code) => {
              setSelectedCountry(code);
              setActiveTab("dashboard");
            }}
          />
        )}

        {/* Map tab */}
        {activeTab === "map" && (
          <MapView
            yearData={yearData}
            selectedMetric={selectedMetric}
            colorScale={colorScale}
            selectedCountry={selectedCountry}
            hoveredCountry={hoveredCountry}
            onCountryClick={(code) => {
              setSelectedCountry(code);
              setActiveTab("dashboard");
            }}
            onCountryHover={setHoveredCountry}
            hoveredData={hoveredCountry ? yearData[hoveredCountry] : null}
            selectedYear={selectedYear}
            minYear={minYear}
            maxYear={maxYear}
            isPlaying={isPlaying}
            onYearChange={setSelectedYear}
            onPlayToggle={handlePlayToggle}
            onMetricChange={setSelectedMetric}
            mobile={mobile}
          />
        )}

        {/* Discovery Logs tab */}
        {activeTab === "agents" && (
          <AgentsView agents={agents} yearData={yearData} mobile={mobile} />
        )}
      </div>

      {/* ---- Footer status bar ---- */}
      <footer
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: mobile ? "10px 16px" : "10px 40px",
          borderTop: `1px solid ${VM.border}`,
          fontFamily: VM.mono,
          fontSize: 10,
          fontWeight: 500,
          letterSpacing: "0.5px",
          textTransform: "uppercase",
          color: VM.textMuted,
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div
            style={{
              width: 6,
              height: 6,
              borderRadius: "50%",
              backgroundColor: "#4CAF50",
            }}
          />
          Agent Network: Active -- {Object.keys(yearData).length} countries
          indexed globally.
        </div>
        {!mobile && (
          <div>
            Data year: {selectedYear} -- All systems operational.
          </div>
        )}
      </footer>
    </div>
  );
}

// ---- Dashboard View ----

function DashboardView({
  display,
  displayLabel,
  displaySubtitle,
  selectedYear,
  availableYears,
  onYearChange,
  agents,
  globalStats,
  activeTab,
  mobile,
  onCountryClick,
}: {
  display: CountryElectricity;
  displayLabel: string;
  displaySubtitle: string;
  selectedYear: number;
  availableYears: number[];
  onYearChange: (year: number) => void;
  agents: AgentInfo[];
  globalStats: ReturnType<typeof Object> | null;
  activeTab: TabKey;
  mobile: boolean;
  onCountryClick: (code: string) => void;
}) {
  const stats = globalStats as {
    totalGen: number;
    totalDemand: number;
    totalEmissions: number;
    ciWeighted: number | null;
    cleanShare: number | null;
    renewShare: number | null;
    top5: CountryElectricity[];
    countryCount: number;
  } | null;

  return (
    <div
      style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: mobile ? "24px 16px" : "40px 48px",
        display: "grid",
        gridTemplateColumns: mobile ? "1fr" : "1fr 340px",
        gap: mobile ? 32 : 56,
        alignItems: "start",
      }}
    >
      {/* Left column */}
      <div>
        {/* Current selection header */}
        <div
          style={{
            fontSize: 10,
            fontFamily: VM.mono,
            fontWeight: 500,
            textTransform: "uppercase",
            letterSpacing: "1px",
            color: VM.textMuted,
            marginBottom: 12,
          }}
        >
          Current Selection
        </div>

        <h1
          style={{
            fontFamily: VM.serif,
            fontSize: mobile ? 32 : 42,
            fontWeight: 400,
            color: VM.text,
            lineHeight: 1.15,
            letterSpacing: "-0.5px",
            margin: "0 0 8px",
          }}
        >
          {displayLabel}
        </h1>
        <p
          style={{
            fontSize: 14,
            color: VM.textMuted,
            lineHeight: 1.5,
            margin: "0 0 32px",
          }}
        >
          {displaySubtitle}
        </p>

        {/* Stat cards 2x2 */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: mobile ? "1fr" : "1fr 1fr",
            gap: 0,
            borderTop: `1px solid ${VM.border}`,
            borderLeft: `1px solid ${VM.border}`,
          }}
        >
          <StatCard
            label="Generation"
            value={fmt(display.generationTotal, 1)}
            unit="TWh"
            subtitle={
              display.generationTotal && display.generationTotal > 100
                ? `${((display.generationTotal / (stats?.totalGen ?? 1)) * 100).toFixed(1)}% of global generation`
                : `Year ${selectedYear}`
            }
          />
          <StatCard
            label="Carbon Intensity"
            value={fmt(display.carbonIntensity, 0)}
            unit={"gCO<sub>2</sub>/kWh"}
            subtitle={
              display.carbonIntensity !== null
                ? display.carbonIntensity < 200
                  ? "Below global average"
                  : "Above global average"
                : ""
            }
          />
          <StatCard
            label="Demand"
            value={fmt(display.demandTotal, 1)}
            unit="TWh"
            subtitle={
              display.demandPerCapita !== null
                ? `${fmt(display.demandPerCapita, 1)} MWh per capita`
                : `Year ${selectedYear}`
            }
          />
          <StatCard
            label="Renewable Share"
            value={fmt(display.shareRenewables, 1)}
            unit="%"
            subtitle={(() => {
              const wind = display.generationMix.wind ?? 0;
              const hydro = display.generationMix.hydro ?? 0;
              const solar = display.generationMix.solar ?? 0;
              const parts: string[] = [];
              if (wind > 0) parts.push(`Wind: ${fmtSub(wind)}`);
              if (hydro > 0) parts.push(`Hydro: ${fmtSub(hydro)}`);
              if (solar > 0) parts.push(`Solar: ${fmtSub(solar)}`);
              return parts.slice(0, 2).join(" / ") + " TWh";
            })()}
          />
        </div>

        {/* Generation mix section (shown in both dashboard and generation tab) */}
        {(activeTab === "generation" || activeTab === "dashboard") && (
          <div style={{ marginTop: 40 }}>
            <div
              style={{
                fontSize: 10,
                fontFamily: VM.mono,
                fontWeight: 500,
                textTransform: "uppercase",
                letterSpacing: "1px",
                color: VM.textMuted,
                marginBottom: 16,
              }}
            >
              Generation Mix
              {display.generationTotal !== null && (
                <span style={{ marginLeft: 12, color: VM.textMid }}>
                  {fmt(display.generationTotal)} TWh total
                </span>
              )}
            </div>
            <GenerationBar country={display} />
          </div>
        )}

        {/* Top producers table (global view only) */}
        {stats && display.countryCode === "WORLD" && (
          <TopProducersTable
            countries={stats.top5}
            selectedYear={selectedYear}
            onCountryClick={onCountryClick}
          />
        )}
      </div>

      {/* Right column -- agents + generation sources */}
      <aside>
        {/* Active Agents */}
        <div
          style={{
            fontSize: 10,
            fontFamily: VM.mono,
            fontWeight: 500,
            textTransform: "uppercase",
            letterSpacing: "1px",
            color: VM.textMuted,
            marginBottom: 20,
          }}
        >
          Active Agents
        </div>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 0,
          }}
        >
          {agents.map((agent) => (
            <div
              key={agent.name}
              style={{
                padding: "16px 0",
                borderBottom: `1px solid ${VM.borderLight}`,
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  marginBottom: 6,
                }}
              >
                <span
                  style={{
                    fontSize: 14,
                    fontWeight: 600,
                    color: VM.text,
                  }}
                >
                  {agent.name}
                </span>
                <StatusBadge status={agent.status} />
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: VM.textMuted,
                  lineHeight: 1.5,
                }}
              >
                {agent.message}
              </div>
            </div>
          ))}
        </div>

        {/* Generation Sources / context */}
        <div style={{ marginTop: 32 }}>
          <div
            style={{
              fontSize: 10,
              fontFamily: VM.mono,
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "1px",
              color: VM.textMuted,
              marginBottom: 16,
            }}
          >
            Generation Sources
          </div>

          <p
            style={{
              fontSize: 14,
              color: VM.text,
              lineHeight: 1.65,
              marginBottom: 20,
            }}
          >
            {display.shareClean !== null && display.shareClean > 50
              ? `Clean sources dominate the electricity mix at ${fmt(display.shareClean, 1)}%, with ${
                  (display.generationMix.hydro ?? 0) > (display.generationMix.wind ?? 0)
                    ? "hydroelectric"
                    : "wind"
                } providing the largest share of low-carbon generation.`
              : `Fossil fuels account for ${fmt(display.shareFossil, 1)}% of generation. The transition to clean electricity is underway across ${stats?.countryCount ?? 0} countries.`}
          </p>

          {display.generationTotal !== null && (
            <div>
              <div
                style={{
                  fontFamily: VM.serif,
                  fontSize: 28,
                  fontWeight: 400,
                  color: VM.text,
                  letterSpacing: "-0.3px",
                }}
              >
                Total: {fmt(display.generationTotal)}{" "}
                <span style={{ fontSize: 14, color: VM.textMid }}>TWh</span>
              </div>
            </div>
          )}
        </div>

        {/* Year selector (compact) */}
        <div style={{ marginTop: 32 }}>
          <div
            style={{
              fontSize: 10,
              fontFamily: VM.mono,
              fontWeight: 500,
              textTransform: "uppercase",
              letterSpacing: "1px",
              color: VM.textMuted,
              marginBottom: 10,
            }}
          >
            Data Year
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <input
              type="range"
              min={availableYears[0]}
              max={availableYears[availableYears.length - 1]}
              value={selectedYear}
              onChange={(e) => onYearChange(parseInt(e.target.value, 10))}
              style={{ flex: 1, accentColor: VM.accent }}
            />
            <span
              style={{
                fontFamily: VM.mono,
                fontSize: 14,
                fontWeight: 600,
                minWidth: 40,
              }}
            >
              {selectedYear}
            </span>
          </div>
        </div>
      </aside>
    </div>
  );
}

// ---- Top Producers Table ----

function TopProducersTable({
  countries,
  selectedYear,
  onCountryClick,
}: {
  countries: CountryElectricity[];
  selectedYear: number;
  onCountryClick: (code: string) => void;
}) {
  return (
    <div style={{ marginTop: 40 }}>
      <div
        style={{
          fontSize: 10,
          fontFamily: VM.mono,
          fontWeight: 500,
          textTransform: "uppercase",
          letterSpacing: "1px",
          color: VM.textMuted,
          marginBottom: 16,
        }}
      >
        Top Producers ({selectedYear})
      </div>
      <div
        style={{
          border: `1px solid ${VM.border}`,
        }}
      >
        {countries.map((c, i) => (
          <div
            key={c.countryCode}
            onClick={() => onCountryClick(c.countryCode)}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "12px 20px",
              borderBottom:
                i < countries.length - 1
                  ? `1px solid ${VM.borderLight}`
                  : "none",
              cursor: "pointer",
              transition: "background-color 0.1s ease",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.backgroundColor = VM.borderLight)
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.backgroundColor = "transparent")
            }
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span
                style={{
                  fontFamily: VM.mono,
                  fontSize: 10,
                  color: VM.textMuted,
                  width: 20,
                }}
              >
                {i + 1}.
              </span>
              <span style={{ fontSize: 13, fontWeight: 500 }}>
                {c.countryName}
              </span>
            </div>
            <div style={{ display: "flex", gap: 24, alignItems: "center" }}>
              <span
                style={{
                  fontFamily: VM.mono,
                  fontSize: 12,
                  fontWeight: 500,
                }}
              >
                {fmt(c.generationTotal)} TWh
              </span>
              <span
                style={{
                  fontFamily: VM.mono,
                  fontSize: 11,
                  color:
                    (c.shareClean ?? 0) > 50
                      ? "#2D8B4E"
                      : VM.textMuted,
                }}
              >
                {fmt(c.shareClean, 0)}% clean
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ---- Map View ----

const METRIC_OPTIONS: { key: MetricKey; label: string }[] = [
  { key: "carbonIntensity", label: "Carbon Intensity" },
  { key: "shareClean", label: "Clean Share" },
  { key: "shareFossil", label: "Fossil Share" },
  { key: "shareRenewables", label: "Renewables" },
  { key: "demandPerCapita", label: "Demand / Capita" },
  { key: "emissionsTotal", label: "CO2 Emissions" },
];

function MapView({
  yearData,
  selectedMetric,
  colorScale,
  selectedCountry,
  hoveredCountry,
  onCountryClick,
  onCountryHover,
  hoveredData,
  selectedYear,
  minYear,
  maxYear,
  isPlaying,
  onYearChange,
  onPlayToggle,
  onMetricChange,
  mobile,
}: {
  yearData: Record<string, CountryElectricity>;
  selectedMetric: MetricKey;
  colorScale: (value: number | null) => string;
  selectedCountry: string | null;
  hoveredCountry: string | null;
  onCountryClick: (code: string) => void;
  onCountryHover: (code: string | null) => void;
  hoveredData: CountryElectricity | null;
  selectedYear: number;
  minYear: number;
  maxYear: number;
  isPlaying: boolean;
  onYearChange: (year: number) => void;
  onPlayToggle: () => void;
  onMetricChange: (metric: MetricKey) => void;
  mobile: boolean;
}) {
  return (
    <div
      style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: mobile ? "16px" : "32px 48px",
      }}
    >
      {/* Metric selector as pills */}
      <div
        style={{
          display: "flex",
          gap: 4,
          marginBottom: 24,
          flexWrap: "wrap",
        }}
      >
        {METRIC_OPTIONS.map((m) => {
          const isActive = m.key === selectedMetric;
          return (
            <button
              key={m.key}
              onClick={() => onMetricChange(m.key)}
              style={{
                padding: "6px 14px",
                borderRadius: 16,
                border: isActive
                  ? `1px solid ${VM.accent}`
                  : `1px solid ${VM.border}`,
                backgroundColor: isActive ? VM.accent : "transparent",
                color: isActive ? VM.white : VM.text,
                fontFamily: VM.sans,
                fontSize: 11,
                fontWeight: 500,
                cursor: "pointer",
              }}
            >
              {m.label}
            </button>
          );
        })}
      </div>

      {/* Map */}
      <div style={{ position: "relative" }}>
        {hoveredData && (
          <div
            style={{
              position: "absolute",
              top: 12,
              left: "50%",
              transform: "translateX(-50%)",
              zIndex: 10,
              backgroundColor: VM.text,
              color: VM.bg,
              padding: "6px 16px",
              borderRadius: 2,
              fontFamily: VM.mono,
              fontSize: 11,
              display: "flex",
              gap: 12,
              pointerEvents: "none",
            }}
          >
            <span style={{ fontWeight: 600 }}>
              {hoveredData.countryName}
            </span>
            <span>
              {hoveredData[selectedMetric] !== null
                ? fmt(hoveredData[selectedMetric] as number)
                : "No data"}
            </span>
          </div>
        )}
        <WorldMap
          countries={yearData}
          metric={selectedMetric}
          colorScale={colorScale}
          selectedCountry={selectedCountry}
          hoveredCountry={hoveredCountry}
          onCountryClick={onCountryClick}
          onCountryHover={onCountryHover}
        />
      </div>

      {/* Controls */}
      <div style={{ marginTop: 16 }}>
        <YearSlider
          year={selectedYear}
          min={minYear}
          max={maxYear}
          isPlaying={isPlaying}
          onYearChange={onYearChange}
          onPlayToggle={onPlayToggle}
        />
        <MapLegend metric={selectedMetric} />
      </div>
    </div>
  );
}

// ---- Agents View ----

function AgentsView({
  agents,
  yearData,
  mobile,
}: {
  agents: AgentInfo[];
  yearData: Record<string, CountryElectricity>;
  mobile: boolean;
}) {
  const countryCount = Object.keys(yearData).length;

  return (
    <div
      style={{
        maxWidth: 800,
        margin: "0 auto",
        padding: mobile ? "24px 16px" : "40px 48px",
      }}
    >
      <div
        style={{
          fontSize: 10,
          fontFamily: VM.mono,
          fontWeight: 500,
          textTransform: "uppercase",
          letterSpacing: "1px",
          color: VM.textMuted,
          marginBottom: 12,
        }}
      >
        Discovery Agent Network
      </div>

      <h2
        style={{
          fontFamily: VM.serif,
          fontSize: 28,
          fontWeight: 400,
          color: VM.text,
          margin: "0 0 8px",
        }}
      >
        How agents discover electricity data
      </h2>
      <p
        style={{
          fontSize: 14,
          color: VM.textMuted,
          lineHeight: 1.6,
          margin: "0 0 32px",
          maxWidth: 600,
        }}
      >
        Instead of manual scrapers, autonomous agents search public APIs,
        validate data quality, and catalog datasets. No brittle HTML parsing --
        agents adapt to schema changes automatically.
      </p>

      {/* Agent cards */}
      <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
        {[
          {
            name: "Agent-EMBER-01",
            status: "Live" as const,
            region: "Global",
            source: "Ember Yearly Electricity Data",
            desc: "Downloads bulk CSV from Google Cloud Storage. Parses 49,000+ rows, filters to country-level data, indexes by fuel type and year. Covers 230+ countries, 2000-present.",
            datasets: 15,
          },
          {
            name: "Agent-IRENA-07",
            status: "Parsing" as const,
            region: "Global",
            source: "IRENA PxWeb API",
            desc: "Queries dynamic table endpoints for renewable capacity and generation. Handles version changes in table names and positional index mapping for technology types.",
            datasets: 17,
          },
          {
            name: "Agent-EIA-03",
            status: "Idle" as const,
            region: "Global",
            source: "EIA International Energy API",
            desc: "Paginated queries for generation and capacity by fuel. Handles 5,000-row pagination limits. Requires API key authentication. Monthly update cycle.",
            datasets: 15,
          },
          {
            name: "Agent-WB-05",
            status: "Syncing" as const,
            region: "Global",
            source: "World Bank Indicators API",
            desc: "Discovers energy indicators (EG.ELC.*) across the World Bank open data catalog. Tracks electricity access, fossil share, transmission losses, and consumption per capita.",
            datasets: 10,
          },
        ].map((agent, i) => (
          <div
            key={agent.name}
            style={{
              padding: "24px 0",
              borderBottom: `1px solid ${VM.borderLight}`,
              display: "grid",
              gridTemplateColumns: mobile ? "1fr" : "200px 1fr",
              gap: mobile ? 8 : 32,
            }}
          >
            <div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  marginBottom: 4,
                }}
              >
                <span
                  style={{ fontSize: 14, fontWeight: 600, color: VM.text }}
                >
                  {agent.name}
                </span>
                <StatusBadge status={agent.status} />
              </div>
              <div
                style={{
                  fontFamily: VM.mono,
                  fontSize: 10,
                  color: VM.textMuted,
                }}
              >
                {agent.datasets} datasets / {agent.region}
              </div>
            </div>
            <div>
              <div
                style={{
                  fontSize: 13,
                  fontWeight: 500,
                  color: VM.text,
                  marginBottom: 4,
                }}
              >
                {agent.source}
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: VM.textMuted,
                  lineHeight: 1.6,
                }}
              >
                {agent.desc}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div
        style={{
          marginTop: 40,
          padding: "24px 28px",
          border: `1px solid ${VM.border}`,
        }}
      >
        <div style={{ display: "flex", gap: 40, flexWrap: "wrap" }}>
          <div>
            <div
              style={{
                fontFamily: VM.serif,
                fontSize: 32,
                fontWeight: 400,
                color: VM.text,
              }}
            >
              {countryCount}
            </div>
            <div
              style={{
                fontFamily: VM.mono,
                fontSize: 10,
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                color: VM.textMuted,
              }}
            >
              Countries indexed
            </div>
          </div>
          <div>
            <div
              style={{
                fontFamily: VM.serif,
                fontSize: 32,
                fontWeight: 400,
                color: VM.text,
              }}
            >
              4
            </div>
            <div
              style={{
                fontFamily: VM.mono,
                fontSize: 10,
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                color: VM.textMuted,
              }}
            >
              Active agents
            </div>
          </div>
          <div>
            <div
              style={{
                fontFamily: VM.serif,
                fontSize: 32,
                fontWeight: 400,
                color: VM.text,
              }}
            >
              57
            </div>
            <div
              style={{
                fontFamily: VM.mono,
                fontSize: 10,
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                color: VM.textMuted,
              }}
            >
              Datasets cataloged
            </div>
          </div>
          <div>
            <div
              style={{
                fontFamily: VM.serif,
                fontSize: 32,
                fontWeight: 400,
                color: VM.text,
              }}
            >
              0
            </div>
            <div
              style={{
                fontFamily: VM.mono,
                fontSize: 10,
                textTransform: "uppercase",
                letterSpacing: "0.5px",
                color: VM.textMuted,
              }}
            >
              Scrapers
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
