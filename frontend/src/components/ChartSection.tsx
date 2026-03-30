import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import LazyChart from "./LazyChart";
import { COLORS, FONTS, SPRING, CHART_TIMING, BUTTON_SECONDARY, BUTTON_ACCENT_OUTLINE } from "../theme";
import type { VizMeta } from "../search";
import { trackChartViewed, trackChartClicked, trackNotebookOpened } from "../analytics";

export default function ChartSection({ viz }: { viz: VizMeta }) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });
  const [stage, setStage] = useState(0);

  useEffect(() => {
    if (!isInView) return;
    trackChartViewed(viz.id, viz.title, viz.chartType);
    const timers: ReturnType<typeof setTimeout>[] = [];
    timers.push(setTimeout(() => setStage(1), CHART_TIMING.title));
    timers.push(setTimeout(() => setStage(2), CHART_TIMING.description));
    timers.push(setTimeout(() => setStage(3), CHART_TIMING.iframe));
    timers.push(setTimeout(() => setStage(4), CHART_TIMING.insights));
    return () => timers.forEach(clearTimeout);
  }, [isInView]);

  return (
    <div ref={ref} style={{ marginBottom: 56 }}>
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: stage >= 1 ? 1 : 0, y: stage >= 1 ? 0 : 8 }}
        transition={SPRING.gentle}
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          marginBottom: 6,
        }}
      >
        <Link
          to={`/viz/${viz.id}`}
          style={{ textDecoration: "none", color: "inherit" }}
          onClick={() => trackChartClicked(viz.id, viz.title, "chart_title")}
        >
          <h2 style={{
            fontSize: 17,
            fontWeight: 600,
            letterSpacing: "-0.3px",
            color: COLORS.text,
            margin: 0,
          }}>
            {viz.title}
          </h2>
        </Link>
        <span style={{
          fontSize: 9,
          fontFamily: FONTS.mono,
          textTransform: "uppercase",
          letterSpacing: "0.3px",
          color: COLORS.textMuted,
          flexShrink: 0,
          marginLeft: 12,
        }}>
          {viz.chartType}
        </span>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: stage >= 2 ? 1 : 0 }}
        transition={{ duration: 0.4 }}
        style={{
          fontSize: 12,
          color: COLORS.textMuted,
          lineHeight: 1.6,
          maxWidth: 600,
          margin: "0 0 14px",
        }}
      >
        {viz.description.split(".")[0]}.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{
          opacity: stage >= 3 ? 1 : 0,
          y: stage >= 3 ? 0 : 16,
        }}
        transition={SPRING.slide}
        style={{
          border: `1px solid ${COLORS.border}`,
          borderRadius: 2,
          overflow: "hidden",
          backgroundColor: COLORS.bg,
        }}
      >
        <LazyChart vizId={viz.id} hideChrome />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: stage >= 3 ? 1 : 0, y: stage >= 3 ? 0 : 6 }}
        transition={SPRING.gentle}
        style={{ display: "flex", gap: 8, marginTop: 10, flexWrap: "wrap" }}
      >
        <Link
          to={`/viz/${viz.id}`}
          style={{ ...BUTTON_SECONDARY, textDecoration: "none" }}
          onClick={() => trackChartClicked(viz.id, viz.title, "open_chart_button")}
        >
          Open Chart
        </Link>
        {viz.notebookPath && (
          <a
            href={`/wasm-notebooks/${viz.id}.html`}
            target="_blank"
            rel="noopener noreferrer"
            style={{ ...BUTTON_ACCENT_OUTLINE, textDecoration: "none" }}
            onClick={() => trackNotebookOpened(viz.id)}
          >
            Marimo Notebook
          </a>
        )}
      </motion.div>

      {viz.highlights.length > 0 && (
        <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 6 }}>
          {viz.highlights.slice(0, 3).map((h, j) => (
            <motion.div
              key={j}
              initial={{ opacity: 0, x: -6 }}
              animate={{
                opacity: stage >= 4 ? 1 : 0,
                x: stage >= 4 ? 0 : -6,
              }}
              transition={{
                ...SPRING.gentle,
                delay: j * (CHART_TIMING.insightGap / 1000),
              }}
              style={{
                fontSize: 11,
                color: COLORS.textMid,
                paddingLeft: 10,
                borderLeft: `2px solid ${COLORS.accent}`,
                lineHeight: 1.5,
              }}
            >
              {h}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
