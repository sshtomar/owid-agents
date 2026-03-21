import React, { useRef, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import { useApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";
import ChartRenderer from "./ChartRenderer";
import SearchBar from "./SearchBar";
import { VizEntry, VizListResponse, THEMES, matchesSearch, matchesTheme } from "../search";

const SPRING = {
  gentle: { type: "spring" as const, stiffness: 300, damping: 30 },
};

function downloadHtml(html: string, filename: string) {
  const blob = new Blob([html], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function GalleryCard({ viz, index }: { viz: VizEntry; index: number }) {
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
            color: "#2B2A27",
          }}>
            {viz.title}
          </div>
          <span style={{
            fontSize: 9,
            fontFamily: "'JetBrains Mono', monospace",
            textTransform: "uppercase",
            letterSpacing: "0.3px",
            color: "#7A786F",
          }}>
            {viz.chartType}
          </span>
        </div>
        <div style={{
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 9,
          color: "#7A786F",
          marginBottom: 10,
        }}>
          {viz.description.split(".")[0]}.
        </div>
        <div style={{
          border: "1px solid #E2E0D5",
          borderRadius: 2,
          overflow: "hidden",
        }}>
          <ChartRenderer html={viz.generatedCode} hideChrome />
        </div>
        {viz.highlights.length > 0 && (
          <div style={{
            fontSize: 11,
            color: "#5A5850",
            paddingLeft: 10,
            borderLeft: "2px solid #EA5E33",
            marginTop: 10,
            lineHeight: 1.5,
          }}>
            {viz.highlights[0]}
          </div>
        )}
      </Link>
      <button
        onClick={(e) => {
          e.stopPropagation();
          downloadHtml(viz.generatedCode, `${viz.id}.html`);
        }}
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 4,
          marginTop: 8,
          padding: "5px 10px",
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 9,
          fontWeight: 500,
          letterSpacing: "0.3px",
          color: "#7A786F",
          backgroundColor: "transparent",
          border: "1px solid #C2C0B5",
          borderRadius: 2,
          textTransform: "uppercase" as const,
          cursor: "pointer",
        }}
      >
        <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#7A786F" strokeWidth="1.5">
          <path d="M6 1v7M3 6l3 3 3-3M1 10h10" />
        </svg>
        Download
      </button>
      {viz.notebookPath && (
        <a
          href={`/wasm-notebooks/${viz.id}.html`}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 4,
            marginTop: 8,
            marginLeft: 8,
            padding: "5px 10px",
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 9,
            fontWeight: 500,
            letterSpacing: "0.3px",
            color: "#EA5E33",
            backgroundColor: "transparent",
            border: "1px solid #EA5E33",
            borderRadius: 2,
            textTransform: "uppercase",
            textDecoration: "none",
          }}
        >
          <svg width="10" height="10" viewBox="0 0 12 12" fill="none" stroke="#EA5E33" strokeWidth="1.5">
            <path d="M2 10h8M6 2v6M3.5 5.5 6 8l2.5-2.5" />
          </svg>
          Marimo Notebook
        </a>
      )}
    </motion.div>
  );
}

export default function VizGallery() {
  const mobile = useIsMobile();
  const { data, loading, error } = useApi<VizListResponse>("/visualizations");
  const [query, setQuery] = useState("");
  const [activeThemes, setActiveThemes] = useState<string[]>([]);

  const vizList = data?.visualizations ?? [];

  const filtered = useMemo(() => {
    return vizList.filter((viz) => {
      const passesQuery = !query || matchesSearch(viz, query);
      const passesTheme = activeThemes.length === 0 ||
        activeThemes.some((label) => matchesTheme(viz, THEMES.find((t) => t.label === label)!));
      return passesQuery && passesTheme;
    });
  }, [vizList, query, activeThemes]);

  if (loading) {
    return (
      <div style={{
        textAlign: "center",
        padding: 64,
        color: "#7A786F",
        fontSize: 11,
        fontFamily: "'JetBrains Mono', monospace",
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
        color: "#7A786F",
        fontSize: 11,
        fontFamily: "'JetBrains Mono', monospace",
      }}>
        Error: {error}
      </div>
    );
  }

  return (
    <div style={{
      padding: mobile ? "20px 16px" : "32px 40px",
      backgroundColor: "#F6F5EE",
      minHeight: "100%",
    }}>
      <div style={{
        marginBottom: 32,
        borderBottom: "1px solid #C2C0B5",
        paddingBottom: 16,
      }}>
        <h1 style={{
          fontSize: 18,
          fontWeight: 600,
          letterSpacing: "-0.3px",
          color: "#2B2A27",
          marginBottom: 4,
        }}>
          All Charts
        </h1>
        <p style={{ fontSize: 12, color: "#7A786F", margin: "0 0 16px" }}>
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
          color: "#7A786F",
          fontSize: 11,
          fontFamily: "'JetBrains Mono', monospace",
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
                color: "#7A786F",
                fontFamily: "'JetBrains Mono', monospace",
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
              <GalleryCard key={viz.id} viz={viz} index={i} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
