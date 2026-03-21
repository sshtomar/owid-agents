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

import React, { useEffect, useRef, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion, useInView } from "framer-motion";
import createGlobe from "cobe";
import { useApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";
import ChartRenderer from "./ChartRenderer";
import SearchBar from "./SearchBar";
import { VizEntry, VizListResponse, THEMES, vizSearchable } from "../search";

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

const PROVIDER_LABELS: Record<string, string> = {
  "world-bank": "World Bank",
  "who-gho": "WHO",
  "un-sdg": "UN SDG",
  eurostat: "Eurostat",
  unhcr: "UNHCR",
  imf: "IMF",
  owid: "OWID",
  unesco: "UNESCO",
};

const PROVIDER_ORDER = [
  "world-bank",
  "who-gho",
  "un-sdg",
  "eurostat",
  "unhcr",
  "imf",
  "owid",
  "unesco",
];

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

/* ── Globe ────────────────────────────────────────────── */

function Globe() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pointerRef = useRef<{ x: number; dragging: boolean }>({ x: 0, dragging: false });
  const phiRef = useRef(0);

  useEffect(() => {
    let autoSpeed = 0.003;
    let animationId: number;

    const globe = createGlobe(canvasRef.current!, {
      devicePixelRatio: Math.min(window.devicePixelRatio, 2),
      width: 520 * 2,
      height: 520 * 2,
      phi: 0,
      theta: 0.15,
      dark: 0,
      diffuse: 1.4,
      mapSamples: 16000,
      mapBrightness: 1.2,
      mapBaseBrightness: 0.05,
      baseColor: [0.96, 0.95, 0.91],
      markerColor: [0.92, 0.37, 0.2],
      glowColor: [0.91, 0.9, 0.85],
      markers: [
        { location: [37.78, -122.44], size: 0.03 },
        { location: [51.51, -0.13], size: 0.03 },
        { location: [35.68, 139.65], size: 0.02 },
        { location: [-33.87, 151.21], size: 0.02 },
        { location: [28.61, 77.21], size: 0.03 },
        { location: [-1.29, 36.82], size: 0.02 },
        { location: [55.75, 37.62], size: 0.02 },
        { location: [-23.55, -46.63], size: 0.03 },
        { location: [46.95, 7.45], size: 0.02 },
        { location: [30.04, 31.24], size: 0.02 },
      ],
      opacity: 0.85,
    });

    const canvas = canvasRef.current!;

    function animate() {
      if (!pointerRef.current.dragging) {
        phiRef.current += autoSpeed;
      }
      globe.update({ phi: phiRef.current });
      animationId = requestAnimationFrame(animate);
    }
    animate();

    const onPointerDown = (e: PointerEvent) => {
      pointerRef.current = { x: e.clientX, dragging: true };
      canvas.setPointerCapture(e.pointerId);
    };

    const onPointerMove = (e: PointerEvent) => {
      if (!pointerRef.current.dragging) return;
      const dx = e.clientX - pointerRef.current.x;
      pointerRef.current.x = e.clientX;
      phiRef.current += dx * 0.01;
    };

    const onPointerUp = () => {
      pointerRef.current.dragging = false;
    };

    canvas.addEventListener("pointerdown", onPointerDown);
    canvas.addEventListener("pointermove", onPointerMove);
    canvas.addEventListener("pointerup", onPointerUp);
    canvas.addEventListener("pointerleave", onPointerUp);

    return () => {
      cancelAnimationFrame(animationId);
      canvas.removeEventListener("pointerdown", onPointerDown);
      canvas.removeEventListener("pointermove", onPointerMove);
      canvas.removeEventListener("pointerup", onPointerUp);
      canvas.removeEventListener("pointerleave", onPointerUp);
      globe.destroy();
    };
  }, []);

  return (
    <motion.canvas
      ref={canvasRef}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.2, delay: 0.3 }}
      style={{
        width: 260,
        height: 260,
        maxWidth: "100%",
        aspectRatio: "1",
        cursor: "grab",
        touchAction: "none",
      }}
    />
  );
}

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

/* ── Agent status (rotating activity messages) ────────── */

const AGENT_ACTIVITIES = [
  "Scanning World Bank API for new economic indicators...",
  "Cross-referencing WHO mortality datasets...",
  "Indexing population demographics by region...",
  "Fetching latest GDP per capita figures...",
  "Analyzing health expenditure trends across 194 countries...",
  "Checking for updated poverty headcount ratios...",
  "Pulling infant mortality rates from WHO GHO...",
  "Comparing education spending indicators year-over-year...",
  "Scanning for new climate-related development metrics...",
  "Validating data completeness for Sub-Saharan Africa...",
  "Refreshing life expectancy time series...",
  "Querying access to clean water indicators...",
];

function AgentStatusSection({ delay }: { delay: number }) {
  const [activityIndex, setActivityIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisible(false);
      setTimeout(() => {
        setActivityIndex((i) => (i + 1) % AGENT_ACTIVITIES.length);
        setVisible(true);
      }, 400);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const elapsed = useMemo(() => {
    const base = Math.floor(Math.random() * 200) + 50;
    return `${base} datasets scanned`;
  }, []);

  return (
    <SidebarSection label="Agent Status" delay={delay}>
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
        minHeight: 34,
        transition: "opacity 0.4s ease",
        opacity: visible ? 1 : 0,
      }}>
        {AGENT_ACTIVITIES[activityIndex]}
      </div>
      <div style={{
        marginTop: 8,
        fontFamily: "'JetBrains Mono', monospace",
        fontSize: 9,
        color: "#A8A69E",
      }}>
        {elapsed}
      </div>
    </SidebarSection>
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
        <ChartRenderer html={viz.generatedCode} hideChrome />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: stage >= 3 ? 1 : 0, y: stage >= 3 ? 0 : 6 }}
        transition={SPRING.gentle}
        style={{ display: "flex", gap: 8, marginTop: 10, flexWrap: "wrap" }}
      >
        <Link
          to={`/viz/${viz.id}`}
          style={{
            display: "inline-flex",
            alignItems: "center",
            padding: "6px 10px",
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 9,
            fontWeight: 500,
            letterSpacing: "0.3px",
            color: "#7A786F",
            border: "1px solid #C2C0B5",
            borderRadius: 2,
            textDecoration: "none",
            textTransform: "uppercase",
          }}
        >
          Open Chart
        </Link>
        {viz.notebookPath && (
          <a
            href={`/wasm-notebooks/${viz.id}.html`}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: "inline-flex",
              alignItems: "center",
              padding: "6px 10px",
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 9,
              fontWeight: 500,
              letterSpacing: "0.3px",
              color: "#EA5E33",
              border: "1px solid #EA5E33",
              borderRadius: 2,
              textDecoration: "none",
              textTransform: "uppercase",
            }}
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
  const mobile = useIsMobile();
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
    return PROVIDER_ORDER.filter((provider) => counts.has(provider)).map((provider) => ({
      provider,
      label: PROVIDER_LABELS[provider] ?? provider,
      count: counts.get(provider) ?? 0,
    }));
  }, [datasets]);

  const filtered = useMemo(() => {
    return vizList.filter((viz) => {
      const text = vizSearchable(viz);
      const passesQuery = !query || text.includes(query.toLowerCase());
      const passesTheme = activeThemes.length === 0 ||
        activeThemes.some((label) =>
          THEMES.find((t) => t.label === label)!.keywords.some((kw) => text.includes(kw))
        );
      return passesQuery && passesTheme;
    });
  }, [vizList, query, activeThemes]);

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
            color: "#2B2A27",
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
              color: "#7A786F",
              lineHeight: 1.6,
              maxWidth: 600,
              margin: 0,
            }}
          >
            Autonomous agents mine the world's open data, surface the stories
            hidden inside, and publish every step of their reasoning.
          </motion.p>

          {/* Search bar */}
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
        </div>

        {!mobile && (
          <div style={{ flexShrink: 0, marginTop: -16 }}>
            <Globe />
          </div>
        )}
      </header>

      {/* Divider */}
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: mobile ? "0 16px" : "0 48px" }}>
        <div style={{ borderTop: "1px solid #C2C0B5" }} />
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
              From 33.4 years in 1960 to 78.0 in 2023. Europe took two centuries
              to make that same gain.
            </div>
          </SidebarSection>

          <SidebarSection label="Data sources" delay={TIMING.sidebarStart + TIMING.sidebarStagger * 3}>
            <div style={{ fontSize: 11, color: "#7A786F", lineHeight: 1.7 }}>
              {providerSummary.map(({ provider, label, count }) => (
                <div key={provider}>
                  <span style={{ color: "#2B2A27", fontWeight: 500 }}>{label}</span>{" "}
                  ({count} {count === 1 ? "indicator" : "indicators"})
                </div>
              ))}
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
        <main style={{ order: mobile ? 0 : 1 }}>
          {filtered.length === 0 && (query || activeThemes.length > 0) ? (
            <div style={{
              padding: "64px 0",
              textAlign: "center",
              color: "#7A786F",
              fontSize: 11,
              fontFamily: "'JetBrains Mono', monospace",
            }}>
              No charts match "{query || activeThemes.join(", ")}". Try a different search.
            </div>
          ) : (
            filtered.map((viz) => (
              <ChartSection key={viz.id} viz={viz} />
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
