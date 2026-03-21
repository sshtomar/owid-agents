import React, { useState } from "react";
import { THEMES } from "../search";

interface SearchBarProps {
  query: string;
  onQueryChange: (q: string) => void;
  activeThemes: string[];
  onThemesChange: (themes: string[]) => void;
  resultCount: number;
  totalCount: number;
}

export default function SearchBar({
  query,
  onQueryChange,
  activeThemes,
  onThemesChange,
  resultCount,
  totalCount,
}: SearchBarProps) {
  const [focused, setFocused] = useState(false);
  const hasFilters = query.length > 0 || activeThemes.length > 0;
  const isFiltered = hasFilters && resultCount !== totalCount;

  function toggleTheme(label: string) {
    if (activeThemes.includes(label)) {
      onThemesChange(activeThemes.filter((t) => t !== label));
    } else {
      onThemesChange([...activeThemes, label]);
    }
  }

  return (
    <div>
      <div style={{
        position: "relative",
        maxWidth: 400,
        marginBottom: 10,
      }}>
        {/* Search icon */}
        <svg
          width="13"
          height="13"
          viewBox="0 0 15 15"
          fill="none"
          style={{
            position: "absolute",
            left: 10,
            top: "50%",
            transform: "translateY(-50%)",
            pointerEvents: "none",
          }}
        >
          <path
            d="M10 6.5a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0ZM9.5 10l3.5 3.5"
            stroke="#7A786F"
            strokeWidth="1.4"
            strokeLinecap="round"
          />
        </svg>
        <input
          type="text"
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder="Search by topic, country, keyword..."
          style={{
            width: "100%",
            padding: "8px 32px 8px 30px",
            fontSize: 12,
            fontFamily: "'JetBrains Mono', monospace",
            backgroundColor: focused ? "#EBEAE2" : "#EEEDE6",
            border: `1px solid ${focused ? "#EA5E33" : "#D5D3C8"}`,
            borderRadius: 3,
            color: "#2B2A27",
            outline: "none",
            boxSizing: "border-box",
            transition: "border-color 0.15s ease, background-color 0.15s ease",
          }}
        />
        {/* Clear button */}
        {query.length > 0 && (
          <button
            onClick={() => onQueryChange("")}
            style={{
              position: "absolute",
              right: 6,
              top: "50%",
              transform: "translateY(-50%)",
              background: "none",
              border: "none",
              cursor: "pointer",
              padding: "2px 4px",
              fontSize: 14,
              color: "#7A786F",
              lineHeight: 1,
              fontFamily: "'JetBrains Mono', monospace",
            }}
            aria-label="Clear search"
          >
            x
          </button>
        )}
      </div>

      {/* Theme chips */}
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center" }}>
        {THEMES.map((theme) => {
          const isActive = activeThemes.includes(theme.label);
          return (
            <ThemeChip
              key={theme.label}
              label={theme.label}
              isActive={isActive}
              onClick={() => toggleTheme(theme.label)}
            />
          );
        })}
        {hasFilters && (
          <>
            <button
              onClick={() => { onQueryChange(""); onThemesChange([]); }}
              style={{
                padding: "4px 8px",
                fontSize: 10,
                fontFamily: "'JetBrains Mono', monospace",
                letterSpacing: "0.2px",
                border: "none",
                borderRadius: 2,
                backgroundColor: "transparent",
                color: "#EA5E33",
                cursor: "pointer",
                marginLeft: 4,
              }}
            >
              Clear all
            </button>
            {isFiltered && (
              <span style={{
                fontSize: 10,
                fontFamily: "'JetBrains Mono', monospace",
                color: "#7A786F",
                marginLeft: 2,
              }}>
                {resultCount} of {totalCount}
              </span>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function ThemeChip({
  label,
  isActive,
  onClick,
}: {
  label: string;
  isActive: boolean;
  onClick: () => void;
}) {
  const [hovered, setHovered] = useState(false);

  const borderColor = isActive
    ? "#EA5E33"
    : hovered
      ? "#9A988F"
      : "#D5D3C8";

  const textColor = isActive
    ? "#fff"
    : hovered
      ? "#2B2A27"
      : "#7A786F";

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        padding: "4px 10px",
        fontSize: 10,
        fontFamily: "'JetBrains Mono', monospace",
        letterSpacing: "0.2px",
        border: `1px solid ${borderColor}`,
        borderRadius: 2,
        backgroundColor: isActive ? "#EA5E33" : "transparent",
        color: textColor,
        cursor: "pointer",
        textTransform: "uppercase",
        transition: "all 0.15s ease",
      }}
    >
      {label}
    </button>
  );
}
