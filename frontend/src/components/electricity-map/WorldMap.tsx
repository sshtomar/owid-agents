import React, { useEffect, useRef, useMemo, useState } from "react";
import { feature } from "topojson-client";
import type { Topology } from "topojson-specification";
import { geoJsonToSvgPaths, type GeoFeature } from "./geo";
import { COLORS } from "../../theme";
import type { CountryElectricity, MetricKey } from "./types";

const TOPOJSON_URL =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

const MAP_WIDTH = 960;
const MAP_HEIGHT = 500;

interface WorldMapProps {
  countries: Record<string, CountryElectricity>;
  metric: MetricKey;
  colorScale: (value: number | null) => string;
  selectedCountry: string | null;
  hoveredCountry: string | null;
  onCountryClick: (code: string) => void;
  onCountryHover: (code: string | null) => void;
}

export default function WorldMap({
  countries,
  metric,
  colorScale,
  selectedCountry,
  hoveredCountry,
  onCountryClick,
  onCountryHover,
}: WorldMapProps) {
  const [geoFeatures, setGeoFeatures] = useState<GeoFeature[]>([]);
  const fetchedRef = useRef(false);

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;

    fetch(TOPOJSON_URL)
      .then((res) => {
        if (!res.ok) throw new Error(`TopoJSON fetch failed: ${res.status}`);
        return res.json();
      })
      .then((topo: Topology) => {
        const countriesGeo = feature(
          topo,
          topo.objects.countries as never,
        ) as unknown as GeoJSON.FeatureCollection;
        const paths = geoJsonToSvgPaths(
          countriesGeo.features as never,
          MAP_WIDTH,
          MAP_HEIGHT,
        );
        setGeoFeatures(paths);
      })
      .catch((err) => {
        console.error("Failed to load world map:", err);
      });
  }, []);

  const fills = useMemo(() => {
    const map = new Map<string, string>();
    for (const feat of geoFeatures) {
      const country = countries[feat.id];
      const value = country ? (country[metric] as number | null) : null;
      map.set(feat.id, colorScale(value));
    }
    return map;
  }, [geoFeatures, countries, metric, colorScale]);

  if (geoFeatures.length === 0) {
    return (
      <div
        style={{
          width: "100%",
          aspectRatio: `${MAP_WIDTH}/${MAP_HEIGHT}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: COLORS.textMuted,
          fontSize: 11,
          fontFamily: "'JetBrains Mono', monospace",
        }}
      >
        Loading map...
      </div>
    );
  }

  return (
    <svg
      viewBox={`0 0 ${MAP_WIDTH} ${MAP_HEIGHT}`}
      style={{ width: "100%", height: "auto", display: "block" }}
    >
      <rect width={MAP_WIDTH} height={MAP_HEIGHT} fill={COLORS.bg} />
      {geoFeatures.map((feat) => {
        const isSelected = feat.id === selectedCountry;
        const isHovered = feat.id === hoveredCountry;
        return (
          <path
            key={feat.id}
            d={feat.pathData}
            fill={fills.get(feat.id) ?? COLORS.inputBg}
            stroke={
              isSelected
                ? COLORS.accent
                : isHovered
                  ? COLORS.text
                  : COLORS.border
            }
            strokeWidth={isSelected ? 1.5 : isHovered ? 0.8 : 0.3}
            style={{
              transition: "fill 0.3s ease",
              cursor: "pointer",
            }}
            onClick={() => onCountryClick(feat.id)}
            onMouseEnter={() => onCountryHover(feat.id)}
            onMouseLeave={() => onCountryHover(null)}
          />
        );
      })}
    </svg>
  );
}
