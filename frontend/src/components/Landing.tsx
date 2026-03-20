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

import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import { useApi } from "../hooks/useApi";
import ChartRenderer from "./ChartRenderer";

interface VizEntry {
  id: string;
  title: string;
  description: string;
  chartType: string;
  highlights: string[];
  generatedCode: string;
}

interface VizListResponse {
  visualizations: VizEntry[];
  count: number;
}

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

/* ── Timing ────────────────────────────────────────────── */

const TIMING = {
  heroSubtitle:   200,    // subtitle appears after page load
  sidebarStart:   400,    // first sidebar section
  sidebarStagger: 200,    // gap between sidebar sections
};

const CHART_TIMING = {
  title:       0,       // chart title appears on scroll
  description: 150,     // description follows
  iframe:      300,     // chart itself
  insights:    700,     // insight bullets begin
  insightGap:  120,     // stagger between bullets
};

/* ── Spring configs ────────────────────────────────────── */

const SPRING = {
  gentle: { type: "spring" as const, stiffness: 300, damping: 30 },
  slide:  { type: "spring" as const, stiffness: 350, damping: 28 },
};

const FADE_UP = {
  offsetY: 16,
};

/* ── Sidebar section ───────────────────────────────────── */

function SidebarSection({
  label,
  children,
  delay,
}: {
  label: string;
  children: React.ReactNode;
  delay: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ ...SPRING.gentle, delay: delay / 1000 }}
      style={{
        borderBottom: "1px solid #E2E0D5",
        paddingBottom: 20,
      }}
    >
      <div style={{
        fontSize: 9,
        textTransform: "uppercase",
        letterSpacing: "0.5px",
        color: "#7A786F",
        marginBottom: 10,
        fontFamily: "'JetBrains Mono', monospace",
      }}>
        {label}
      </div>
      {children}
    </motion.div>
  );
}

/* ── Agent log entry ───────────────────────────────────── */

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
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 10,
        color: "#7A786F",
        display: "flex",
        alignItems: "flex-start",
        gap: 6,
        marginBottom: 4,
      }}>
        <span style={{ color: "#EA5E33", flexShrink: 0 }}>{">"}</span>
        <span>{action}</span>
      </div>
      <div style={{
        fontSize: 12,
        fontWeight: 500,
        color: "#2B2A27",
        lineHeight: 1.5,
        marginBottom: detail ? 4 : 0,
      }}>
        {result}
      </div>
      {detail && (
        <div style={{
          fontSize: 11,
          color: "#7A786F",
          lineHeight: 1.5,
        }}>
          {detail}
        </div>
      )}
    </div>
  );
}

/* ── Chart section ─────────────────────────────────────── */

function ChartSection({ viz }: { viz: VizEntry }) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "-80px" });
  const [stage, setStage] = useState(0);

  useEffect(() => {
    if (!isInView) return;
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
        >
          <h2 style={{
            fontSize: 17,
            fontWeight: 600,
            letterSpacing: "-0.3px",
            color: "#2B2A27",
            margin: 0,
          }}>
            {viz.title}
          </h2>
        </Link>
        <span style={{
          fontSize: 9,
          fontFamily: "'JetBrains Mono', monospace",
          textTransform: "uppercase",
          letterSpacing: "0.3px",
          color: "#7A786F",
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
          color: "#7A786F",
          lineHeight: 1.6,
          maxWidth: 600,
          margin: "0 0 14px",
        }}
      >
        {viz.description.split(".")[0]}.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: FADE_UP.offsetY }}
        animate={{
          opacity: stage >= 3 ? 1 : 0,
          y: stage >= 3 ? 0 : FADE_UP.offsetY,
        }}
        transition={SPRING.slide}
        style={{
          border: "1px solid #E2E0D5",
          borderRadius: 2,
          overflow: "hidden",
          backgroundColor: "#F6F5EE",
        }}
      >
        <ChartRenderer html={viz.generatedCode} />
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
                color: "#5A5850",
                paddingLeft: 10,
                borderLeft: "2px solid #EA5E33",
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

/* ── Landing page ──────────────────────────────────────── */

export default function Landing() {
  const vizResp = useApi<VizListResponse>("/visualizations");
  const dsResp = useApi<DatasetsResponse>("/datasets");

  useEffect(() => {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href =
      "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap";
    document.head.appendChild(link);
    return () => { document.head.removeChild(link); };
  }, []);

  const vizList = vizResp.data?.visualizations ?? [];
  const datasets = dsResp.data?.datasets ?? [];
  const totalPoints = datasets.reduce((sum, d) => sum + d.dataPointCount, 0);

  if (vizResp.loading || dsResp.loading) {
    return (
      <div style={{
        backgroundColor: "#F6F5EE",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 11,
        color: "#7A786F",
      }}>
        Loading...
      </div>
    );
  }

  return (
    <div style={{
      backgroundColor: "#F6F5EE",
      color: "#2B2A27",
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
      WebkitFontSmoothing: "antialiased",
      minHeight: "100vh",
    }}>
      {/* Hero */}
      <header style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: "56px 48px 32px",
      }}>
        <h1 style={{
          fontSize: 26,
          fontWeight: 700,
          letterSpacing: "-0.5px",
          lineHeight: 1.2,
          color: "#2B2A27",
          margin: "0 0 10px",
        }}>
          Agents exploring the world's data
        </h1>
        <motion.p
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ ...SPRING.gentle, delay: TIMING.heroSubtitle / 1000 }}
          style={{
            fontSize: 14,
            color: "#7A786F",
            lineHeight: 1.6,
            maxWidth: 600,
            margin: 0,
          }}
        >
          Agents search public databases, find the most interesting datasets,
          and build charts from what they discover.
        </motion.p>
      </header>

      {/* Divider */}
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 48px" }}>
        <div style={{ borderTop: "1px solid #C2C0B5" }} />
      </div>

      {/* Two-column layout */}
      <div style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: "40px 48px 32px",
        display: "grid",
        gridTemplateColumns: "260px 1fr",
        gap: 56,
        alignItems: "start",
      }}>
        {/* Sidebar */}
        <aside style={{
          position: "sticky",
          top: 32,
          display: "flex",
          flexDirection: "column",
          gap: 20,
        }}>
          <SidebarSection label="Agent Status" delay={TIMING.sidebarStart}>
            <div style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 10,
            }}>
              <div style={{
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}>
                <motion.div
                  animate={{ opacity: [1, 0.3, 1] }}
                  transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  style={{
                    width: 6,
                    height: 6,
                    borderRadius: "50%",
                    backgroundColor: "#EA5E33",
                    flexShrink: 0,
                  }}
                />
                <span style={{
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 10,
                  fontWeight: 500,
                  color: "#2B2A27",
                }}>
                  Running
                </span>
              </div>
              <span style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 9,
                color: "#7A786F",
              }}>
                v1.0.0
              </span>
            </div>
            <div style={{
              fontSize: 11,
              color: "#7A786F",
              lineHeight: 1.5,
            }}>
              Currently scanning public health and economic databases for new indicators.
            </div>
          </SidebarSection>

          <SidebarSection label="What it found so far" delay={TIMING.sidebarStart + TIMING.sidebarStagger}>
            <AgentEntry
              action="Searched World Bank and WHO APIs"
              result={`Found ${datasets.length} datasets spanning 1960 to 2024, covering ${
                totalPoints > 1000 ? (totalPoints / 1000).toFixed(0) + "k" : totalPoints
              } data points across 150+ countries.`}
            />
            <AgentEntry
              action="Looked for patterns worth showing"
              result={`Built ${vizList.length} charts from the most striking trends -- convergence in health, the closing digital divide, and the relationship between wealth and longevity.`}
            />
          </SidebarSection>

          <SidebarSection label="Key finding" delay={TIMING.sidebarStart + TIMING.sidebarStagger * 2}>
            <div style={{
              fontSize: 13,
              fontWeight: 500,
              color: "#2B2A27",
              lineHeight: 1.5,
              marginBottom: 6,
            }}>
              China gained 44.5 years of life expectancy in 63 years.
            </div>
            <div style={{
              fontSize: 11,
              color: "#7A786F",
              lineHeight: 1.5,
            }}>
              From 33.4 years in 1960 to 78.0 in 2023 -- compressing two centuries
              of European progress into a single lifetime.
            </div>
          </SidebarSection>

          <SidebarSection label="Data sources" delay={TIMING.sidebarStart + TIMING.sidebarStagger * 3}>
            <div style={{ fontSize: 11, color: "#7A786F", lineHeight: 1.7 }}>
              <div>
                <span style={{ color: "#2B2A27", fontWeight: 500 }}>World Bank</span>{" "}
                -- 8 indicators
              </div>
              <div>
                <span style={{ color: "#2B2A27", fontWeight: 500 }}>WHO</span>{" "}
                -- healthy life expectancy
              </div>
            </div>
          </SidebarSection>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4, delay: (TIMING.sidebarStart + TIMING.sidebarStagger * 4) / 1000 }}
            style={{ display: "flex", gap: 20 }}
          >
            <Link to="/gallery" style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10,
              color: "#EA5E33",
              textDecoration: "none",
              letterSpacing: "0.3px",
            }}>
              Gallery {"->"}
            </Link>
            <Link to="/datasets" style={{
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10,
              color: "#EA5E33",
              textDecoration: "none",
              letterSpacing: "0.3px",
            }}>
              Datasets {"->"}
            </Link>
          </motion.div>
        </aside>

        {/* Charts */}
        <main>
          {vizList.map((viz) => (
            <ChartSection key={viz.id} viz={viz} />
          ))}
        </main>
      </div>

      {/* Footer */}
      <footer style={{
        maxWidth: 1200,
        margin: "0 auto",
        padding: "0 48px 40px",
      }}>
        <div style={{
          borderTop: "1px solid #C2C0B5",
          paddingTop: 16,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}>
          <span style={{
            fontSize: 10,
            fontFamily: "'JetBrains Mono', monospace",
            color: "#7A786F",
          }}>
            Data: World Bank, WHO Global Health Observatory
          </span>
        </div>
      </footer>
    </div>
  );
}
