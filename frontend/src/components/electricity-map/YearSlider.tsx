import React from "react";
import { COLORS, FONTS } from "../../theme";

interface YearSliderProps {
  year: number;
  min: number;
  max: number;
  isPlaying: boolean;
  onYearChange: (year: number) => void;
  onPlayToggle: () => void;
}

export default function YearSlider({
  year,
  min,
  max,
  isPlaying,
  onYearChange,
  onPlayToggle,
}: YearSliderProps) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <button
        onClick={onPlayToggle}
        style={{
          width: 32,
          height: 32,
          borderRadius: 2,
          border: `1px solid ${COLORS.borderStrong}`,
          backgroundColor: isPlaying ? COLORS.accent : "transparent",
          color: isPlaying ? COLORS.white : COLORS.text,
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontFamily: FONTS.mono,
          fontSize: 14,
          flexShrink: 0,
        }}
        title={isPlaying ? "Pause" : "Play"}
      >
        {isPlaying ? "\u2016" : "\u25B6"}
      </button>
      <input
        type="range"
        min={min}
        max={max}
        value={year}
        onChange={(e) => onYearChange(parseInt(e.target.value, 10))}
        style={{
          flex: 1,
          accentColor: COLORS.accent,
          height: 4,
          cursor: "pointer",
        }}
      />
      <span
        style={{
          fontFamily: FONTS.mono,
          fontSize: 16,
          fontWeight: 600,
          color: COLORS.text,
          minWidth: 44,
          textAlign: "right",
        }}
      >
        {year}
      </span>
    </div>
  );
}
