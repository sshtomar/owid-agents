import React, { useEffect, useRef, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import { useApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";
import LazyChart from "./LazyChart";
import ErrorBoundary from "./ErrorBoundary";
import SearchBar from "./SearchBar";
import {
  COLORS, FONTS, SPRING, BUTTON_SECONDARY, BUTTON_ACCENT_OUTLINE,
  relativeTime,
} from "../theme";
import {
  VizMeta, VizListResponse, THEMES,
  createFuseIndex, fuzzySearch, matchesTheme, vizSearchable,
} from "../search";
import { trackSearch, trackThemeFilter, trackChartClicked, trackNotebookOpened } from "../analytics";

function GalleryCard({ viz, index }: { viz: VizMeta; index: number }) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-60px" });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 16 }}
      animate={{
        opacity: isInView ? 1 : 0,
        y: isInView ? 0 : 16,
      }}
      transition={{ ...SPRING.gentle, delay: (index % 2) * 0.1 }}
    >
      <Link
        to={`/viz/${viz.id}`}
        style={{ textDecoration: "none", color: "inherit", display: "block" }}
        onClick={() => trackChartClicked(viz.id, viz.title, "gallery_card")}
      >
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          marginBottom: 4,
        }}>
          <div style={{
            fontSize: 14,
            fontWeight: 600,
            letterSpacing: "-0.2px",
            color: COLORS.text,
          }}>
            {viz.title}
          </div>
          <span style={{
            fontSize: 9,
            fontFamily: FONTS.mono,
            textTransform: "uppercase",
            letterSpacing: "0.3px",
            color: COLORS.textMuted,
          }}>
            {viz.chartType}
          </span>
        </div>
        <div style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          marginBottom: 10,
        }}>
          <div style={{
            fontFamily: FONTS.mono,
            fontSize: 9,
            color: COLORS.textMuted,
          }}>
            {viz.description.split(".")[0]}.
          </div>
          <span style={{
            fontFamily: FONTS.mono,
            fontSize: 8,
            color: COLORS.textSubtle,
            flexShrink: 0,
            marginLeft: 8,
          }}>
            {relativeTime(viz.createdAt)}
          </span>
        </div>
        <div style={{
          border: `1px solid ${COLORS.border}`,
          borderRadius: 2,
          overflow: "hidden",
        }}>
          <LazyChart vizId={viz.id} hideChrome />
        </div>
        {viz.highlights.length > 0 && (
          <div style={{
            fontSize: 11,
            color: COLORS.textMid,
            paddingLeft: 10,
            borderLeft: `2px solid ${COLORS.accent}`,
            marginTop: 10,
            lineHeight: 1.5,
          }}>
            {viz.highlights[0]}
          </div>
        )}
      </Link>
      <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
        {viz.notebookPath && (
          <a
            href={`/wasm-notebooks/${viz.id}.html`}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => { e.stopPropagation(); trackNotebookOpened(viz.id); }}
            style={{ ...BUTTON_ACCENT_OUTLINE, textDecoration: "none", padding: "5px 10px", fontSize: 9, gap: 4 }}
          >
            <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke={COLORS.accent} strokeWidth="1.5">
              <path d="M2 10h8M6 2v6M3.5 5.5 6 8l2.5-2.5" />
            </svg>
            Marimo Notebook
          </a>
        )}
      </div>
    </motion.div>
  );
}

export default function VizGallery() {
  const mobile = useIsMobile();
  const { data, loading, error } = useApi<VizListResponse>("/visualizations");
  const [query, setQuery] = useState("");
  const [activeThemes, setActiveThemes] = useState<string[]>([]);

  const vizList = data?.visualizations ?? [];
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
        activeThemes.some((label) => matchesTheme(viz, THEMES.find((t) => t.label === label)!))
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

  if (loading) {
    return (
      <div style={{
        textAlign: "center",
        padding: 64,
        color: COLORS.textMuted,
        fontSize: 11,
        fontFamily: FONTS.mono,
      }}>
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        textAlign: "center",
        padding: 64,
        color: COLORS.textMuted,
        fontSize: 11,
        fontFamily: FONTS.mono,
      }}>
        Error: {error}
      </div>
    );
  }

  return (
    <div style={{
      padding: mobile ? "20px 16px" : "32px 40px",
      backgroundColor: COLORS.bg,
      minHeight: "100%",
    }}>
      <div style={{
        marginBottom: 32,
        borderBottom: `1px solid ${COLORS.borderStrong}`,
        paddingBottom: 16,
      }}>
        <h1 style={{
          fontSize: 18,
          fontWeight: 600,
          letterSpacing: "-0.3px",
          color: COLORS.text,
          marginBottom: 4,
        }}>
          All Charts
        </h1>
        <p style={{ fontSize: 12, color: COLORS.textMuted, margin: "0 0 16px" }}>
          {vizList.length} visualizations from public datasets
        </p>

        <SearchBar
          query={query}
          onQueryChange={setQuery}
          activeThemes={activeThemes}
          onThemesChange={setActiveThemes}
          resultCount={filtered.length}
          totalCount={vizList.length}
        />
      </div>

      {filtered.length === 0 ? (
        <div style={{
          textAlign: "center",
          padding: 64,
          color: COLORS.textMuted,
          fontSize: 11,
          fontFamily: FONTS.mono,
        }}>
          {vizList.length === 0
            ? "No visualizations yet."
            : `No charts match "${query || activeThemes.join(", ")}". Try a different search.`}
        </div>
      ) : (
        <>
          {(query || activeThemes.length > 0) && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.2 }}
              style={{
                fontSize: 11,
                color: COLORS.textMuted,
                fontFamily: FONTS.mono,
                marginBottom: 20,
              }}
            >
              {filtered.length} of {vizList.length} charts
            </motion.div>
          )}
          <div style={{
            display: "grid",
            gridTemplateColumns: mobile
              ? "1fr"
              : "repeat(auto-fill, minmax(500px, 1fr))",
            gap: mobile ? 32 : 40,
          }}>
            {filtered.map((viz, i) => (
              <ErrorBoundary key={viz.id}>
                <GalleryCard viz={viz} index={i} />
              </ErrorBoundary>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
