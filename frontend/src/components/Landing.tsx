/* ─────────────────────────────────────────────────────────
 * ANIMATION STORYBOARD
 *
 *    0ms   page loads, hero title visible immediately
 *  200ms   hero subtitle fades in, slides up 12px
 *  400ms   sidebar sections stagger in (200ms apart)
 *
 * Per chart (triggered by scrolling into view):
 *    0ms   chart title fades in
 *  150ms   chart description fades in
 *  300ms   chart iframe fades in, slides up 16px
 *  700ms   insight bullets stagger in (120ms apart)
 * ───────────────────────────────────────────────────────── */

import React, { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";
import Globe from "./Globe";
import SearchBar from "./SearchBar";
import SidebarSection from "./SidebarSection";
import AgentStatusSection from "./AgentStatusSection";
import DatasetRequestForm from "./DatasetRequestForm";
import ChartSection from "./ChartSection";
import ErrorBoundary from "./ErrorBoundary";
import {
  COLORS, FONTS, SPRING, TIMING,
  PROVIDER_LABELS, PROVIDER_ORDER,
} from "../theme";
import {
  VizMeta, VizListResponse, THEMES,
  createFuseIndex, fuzzySearch, matchesTheme, vizSearchable,
} from "../search";
import { trackSearch, trackThemeFilter, trackNavigation } from "../analytics";

interface DatasetsResponse {
  datasets: Array<{
    id: string;
    title: string;
    dataPointCount: number;
    source: { provider: string };
    topics: string[];
  }>;
  count: number;
}

function AgentEntry({
  action,
  result,
  detail,
}: {
  action: string;
  result: string;
  detail?: string;
}) {
  return (
    <div style={{ marginBottom: 16 }}>
      <div style={{
        fontFamily: FONTS.mono,
        fontSize: 10,
        color: COLORS.textMuted,
        display: "flex",
        alignItems: "flex-start",
        gap: 6,
        marginBottom: 4,
      }}>
        <span style={{ color: COLORS.accent, flexShrink: 0 }}>{">"}</span>
        <span>{action}</span>
      </div>
      <div style={{
        fontSize: 12,
        fontWeight: 500,
        color: COLORS.text,
        lineHeight: 1.5,
        marginBottom: detail ? 4 : 0,
      }}>
        {result}
      </div>
      {detail && (
        <div style={{ fontSize: 11, color: COLORS.textMuted, lineHeight: 1.5 }}>
          {detail}
        </div>
      )}
    </div>
  );
}

export default function Landing() {
  const mobile = useIsMobile();
  const vizResp = useApi<VizListResponse>("/visualizations");
  const dsResp = useApi<DatasetsResponse>("/datasets");

  const [query, setQuery] = useState("");
  const [activeThemes, setActiveThemes] = useState<string[]>([]);

  const vizList = vizResp.data?.visualizations ?? [];
  const datasets = dsResp.data?.datasets ?? [];
  const totalPoints = datasets.reduce((sum, d) => sum + d.dataPointCount, 0);

  const providerSummary = useMemo(() => {
    const counts = new Map<string, number>();
    for (const ds of datasets) {
      counts.set(ds.source.provider, (counts.get(ds.source.provider) ?? 0) + 1);
    }
    return PROVIDER_ORDER.filter((p) => counts.has(p)).map((p) => ({
      provider: p,
      label: PROVIDER_LABELS[p] ?? p,
      count: counts.get(p) ?? 0,
    }));
  }, [datasets]);

  const fuseIndex = useMemo(() => createFuseIndex(vizList), [vizList]);

  const filtered = useMemo(() => {
    let results = vizList;
    if (query) {
      const fuzzyResults = fuzzySearch(fuseIndex, query);
      results = fuzzyResults.length > 0 ? fuzzyResults : results.filter(
        (v) => vizSearchable(v).includes(query.toLowerCase())
      );
    }
    if (activeThemes.length > 0) {
      results = results.filter((viz) =>
        activeThemes.some((label) =>
          matchesTheme(viz, THEMES.find((t) => t.label === label)!)
        )
      );
    }
    return results;
  }, [vizList, query, activeThemes, fuseIndex]);

  const searchTimer = useRef<ReturnType<typeof setTimeout>>();
  useEffect(() => {
    if (!query) return;
    clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => {
      trackSearch(query, filtered.length, vizList.length);
    }, 800);
    return () => clearTimeout(searchTimer.current);
  }, [query, filtered.length, vizList.length]);

  useEffect(() => {
    if (activeThemes.length > 0) {
      trackThemeFilter(activeThemes, filtered.length);
    }
  }, [activeThemes, filtered.length]);

  if (vizResp.loading || dsResp.loading) {
    return (
      <div style={{
        backgroundColor: COLORS.bg,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        fontFamily: FONTS.mono,
        fontSize: 11,
        color: COLORS.textMuted,
      }}>
        Loading...
      </div>
    );
  }

  return (
    <div style={{
      backgroundColor: COLORS.bg,
      color: COLORS.text,
      fontFamily: FONTS.sans,
      WebkitFontSmoothing: "antialiased",
      minHeight: "100vh",
    }}>
      {/* Hero */}
      <header style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: mobile ? "32px 16px 24px" : "56px 48px 32px",
        display: "flex",
        flexDirection: mobile ? "column" : "row",
        justifyContent: "space-between",
        alignItems: mobile ? "center" : "flex-start",
        gap: mobile ? 24 : 40,
      }}>
        <div style={{ flex: 1, width: mobile ? "100%" : undefined }}>
          <h1 style={{
            fontSize: 26,
            fontWeight: 700,
            letterSpacing: "-0.5px",
            lineHeight: 1.2,
            color: COLORS.text,
            margin: "0 0 10px",
          }}>
            Fieldnotes
          </h1>
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...SPRING.gentle, delay: TIMING.heroSubtitle / 1000 }}
            style={{
              fontSize: 14,
              color: COLORS.textMuted,
              lineHeight: 1.6,
              maxWidth: 600,
              margin: 0,
            }}
          >
            Autonomous agents mine the world's open data, surface the stories
            hidden inside, and publish every step of their reasoning.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ ...SPRING.gentle, delay: 0.35 }}
            style={{ marginTop: 20 }}
          >
            <SearchBar
              query={query}
              onQueryChange={setQuery}
              activeThemes={activeThemes}
              onThemesChange={setActiveThemes}
              resultCount={filtered.length}
              totalCount={vizList.length}
            />
          </motion.div>

          <div style={{ display: "flex", gap: 20, marginTop: 12 }}>
            <Link to="/gallery" onClick={() => trackNavigation("gallery")} style={{
              fontFamily: FONTS.mono,
              fontSize: 10,
              color: COLORS.accent,
              textDecoration: "none",
              letterSpacing: "0.3px",
            }}>
              Gallery {"->"}
            </Link>
            <Link to="/datasets" onClick={() => trackNavigation("datasets")} style={{
              fontFamily: FONTS.mono,
              fontSize: 10,
              color: COLORS.accent,
              textDecoration: "none",
              letterSpacing: "0.3px",
            }}>
              Datasets {"->"}
            </Link>
          </div>
        </div>

        {!mobile && (
          <div style={{ flexShrink: 0, marginTop: -16 }}>
            <Globe />
          </div>
        )}
      </header>

      {/* Divider */}
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: mobile ? "0 16px" : "0 48px" }}>
        <div style={{ borderTop: `1px solid ${COLORS.borderStrong}` }} />
      </div>

      {/* Two-column layout */}
      <div style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: mobile ? "24px 16px 24px" : "40px 48px 32px",
        display: "grid",
        gridTemplateColumns: mobile ? "1fr" : "260px 1fr",
        gap: mobile ? 32 : 56,
        alignItems: "start",
      }}>
        {/* Sidebar */}
        <aside style={{
          position: mobile ? "static" : "sticky",
          top: 32,
          display: "flex",
          flexDirection: "column",
          gap: 20,
          order: mobile ? 1 : 0,
        }}>
          <AgentStatusSection delay={TIMING.sidebarStart} />

          <SidebarSection label="What it found today" delay={TIMING.sidebarStart + TIMING.sidebarStagger}>
            <AgentEntry
              action="Searched World Bank and WHO APIs"
              result={`Found ${datasets.length} datasets spanning 1960 to 2024, covering ${
                totalPoints > 1000 ? (totalPoints / 1000).toFixed(0) + "k" : totalPoints
              } data points across 150+ countries.`}
            />
            <AgentEntry
              action="Looked for patterns worth showing"
              result={`Built ${vizList.length} charts on health convergence, the closing digital divide, and wealth vs. longevity.`}
            />
          </SidebarSection>

          <SidebarSection label="Key finding" delay={TIMING.sidebarStart + TIMING.sidebarStagger * 2}>
            <div style={{
              fontSize: 13,
              fontWeight: 500,
              color: COLORS.text,
              lineHeight: 1.5,
              marginBottom: 6,
            }}>
              China gained 44.5 years of life expectancy in 63 years.
            </div>
            <div style={{
              fontSize: 11,
              color: COLORS.textMuted,
              lineHeight: 1.5,
            }}>
              From 33.4 years in 1960 to 78.0 in 2023. Europe took two centuries
              to make that same gain.
            </div>
          </SidebarSection>

          <SidebarSection label="Data sources" delay={TIMING.sidebarStart + TIMING.sidebarStagger * 3}>
            <div style={{ fontSize: 11, color: COLORS.textMuted, lineHeight: 1.7 }}>
              {providerSummary.map(({ provider, label, count }) => (
                <div key={provider}>
                  <span style={{ color: COLORS.text, fontWeight: 500 }}>{label}</span>{" "}
                  ({count} {count === 1 ? "indicator" : "indicators"})
                </div>
              ))}
            </div>
          </SidebarSection>

          <DatasetRequestForm delay={TIMING.sidebarStart + TIMING.sidebarStagger * 4} />
        </aside>

        {/* Charts */}
        <main style={{ order: mobile ? 0 : 1 }}>
          {filtered.length === 0 && (query || activeThemes.length > 0) ? (
            <div style={{
              padding: "64px 0",
              textAlign: "center",
              color: COLORS.textMuted,
              fontSize: 11,
              fontFamily: FONTS.mono,
            }}>
              No charts match "{query || activeThemes.join(", ")}". Try a different search.
            </div>
          ) : (
            filtered.map((viz) => (
              <ErrorBoundary key={viz.id}>
                <ChartSection viz={viz} />
              </ErrorBoundary>
            ))
          )}
        </main>
      </div>

      {/* Footer */}
      <footer style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: mobile ? "0 16px 32px" : "0 48px 40px",
      }}>
        <div style={{
          borderTop: `1px solid ${COLORS.borderStrong}`,
          paddingTop: 16,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}>
          <span style={{
            fontSize: 10,
            fontFamily: FONTS.mono,
            color: COLORS.textMuted,
          }}>
            Data: World Bank, WHO Global Health Observatory
          </span>
        </div>
      </footer>
    </div>
  );
}
