import type { CSSProperties } from "react";

// --- Colors ---

export const COLORS = {
  bg: "#F6F5EE",
  text: "#2B2A27",
  textMuted: "#7A786F",
  textSubtle: "#A8A69E",
  textMid: "#5A5850",
  accent: "#EA5E33",
  border: "#E2E0D5",
  borderStrong: "#C2C0B5",
  inputBg: "#EEEDE6",
  inputBgFocus: "#EBEAE2",
  badgeBg: "#EEEDE6",
  badgeText: "#5A5850",
  topicBg: "#EEEDE6",
  topicText: "#8B7355",
  white: "#fff",
} as const;

// --- Fonts ---

export const FONTS = {
  mono: "'JetBrains Mono', monospace",
  sans: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
} as const;

// --- Common style patterns ---

export const LABEL_STYLE: CSSProperties = {
  fontSize: 9,
  textTransform: "uppercase",
  letterSpacing: "0.5px",
  color: COLORS.textMuted,
  fontFamily: FONTS.mono,
};

export const MONO_SMALL: CSSProperties = {
  fontFamily: FONTS.mono,
  fontSize: 10,
  fontWeight: 500,
  letterSpacing: "0.3px",
};

export const BUTTON_BASE: CSSProperties = {
  ...MONO_SMALL,
  padding: "6px 12px",
  borderRadius: 2,
  cursor: "pointer",
  textTransform: "uppercase",
  display: "inline-flex",
  alignItems: "center",
};

export const BUTTON_PRIMARY: CSSProperties = {
  ...BUTTON_BASE,
  color: COLORS.white,
  backgroundColor: COLORS.accent,
  border: `1px solid ${COLORS.accent}`,
};

export const BUTTON_SECONDARY: CSSProperties = {
  ...BUTTON_BASE,
  color: COLORS.textMuted,
  backgroundColor: "transparent",
  border: `1px solid ${COLORS.borderStrong}`,
};

export const BUTTON_ACCENT_OUTLINE: CSSProperties = {
  ...BUTTON_BASE,
  color: COLORS.accent,
  backgroundColor: "transparent",
  border: `1px solid ${COLORS.accent}`,
};

// --- Animation timing ---

export const TIMING = {
  heroSubtitle: 200,
  sidebarStart: 400,
  sidebarStagger: 200,
};

export const CHART_TIMING = {
  title: 0,
  description: 150,
  iframe: 300,
  insights: 700,
  insightGap: 120,
};

export const SPRING = {
  gentle: { type: "spring" as const, stiffness: 300, damping: 30 },
  slide: { type: "spring" as const, stiffness: 350, damping: 28 },
};

// --- Provider labels ---

export const PROVIDER_LABELS: Record<string, string> = {
  "world-bank": "World Bank",
  "who-gho": "WHO",
  "un-sdg": "UN SDG",
  eurostat: "Eurostat",
  unhcr: "UNHCR",
  imf: "IMF",
  owid: "OWID",
  unesco: "UNESCO",
};

export const PROVIDER_ORDER = [
  "world-bank",
  "who-gho",
  "un-sdg",
  "eurostat",
  "unhcr",
  "imf",
  "owid",
  "unesco",
];

// --- Relative time helper ---

export function relativeTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return "today";
  if (diffDays === 1) return "yesterday";
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
  return `${Math.floor(diffDays / 365)} years ago`;
}
