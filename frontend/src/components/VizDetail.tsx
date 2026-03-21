import React from "react";
import { useParams, Link } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";
import ChartRenderer from "./ChartRenderer";

interface VizDetailData {
  id: string;
  title: string;
  description: string;
  datasetIds: string[];
  chartType: string;
  highlights: string[];
  createdAt: string;
  htmlCode: string;
  notebookPath?: string;
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: "32px 40px",
    maxWidth: 960,
    backgroundColor: "#F6F5EE",
    minHeight: "100%",
  },
  backLink: {
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 10,
    color: "#EA5E33",
    textDecoration: "none",
    letterSpacing: "0.3px",
    display: "inline-block",
    marginBottom: 20,
  },
  title: {
    fontSize: 18,
    fontWeight: 600,
    letterSpacing: "-0.3px",
    color: "#2B2A27",
    marginBottom: 6,
  },
  desc: {
    fontSize: 11,
    color: "#7A786F",
    lineHeight: 1.6,
    marginBottom: 24,
    maxWidth: 600,
  },
  chartFrame: {
    border: "1px solid #E2E0D5",
    borderRadius: 2,
    overflow: "hidden",
    marginBottom: 24,
    position: "relative",
  },
  meta: {
    display: "flex",
    gap: 32,
    marginBottom: 24,
    borderBottom: "1px solid #C2C0B5",
    paddingBottom: 16,
  },
  metaLabel: {
    fontSize: 9,
    textTransform: "uppercase" as const,
    color: "#7A786F",
    fontWeight: 500,
    fontFamily: "'JetBrains Mono', monospace",
    letterSpacing: "0.3px",
    marginBottom: 4,
  },
  metaValue: {
    fontSize: 11,
    fontWeight: 500,
    color: "#2B2A27",
  },
  sectionLabel: {
    fontSize: 9,
    textTransform: "uppercase" as const,
    fontWeight: 500,
    fontFamily: "'JetBrains Mono', monospace",
    letterSpacing: "0.3px",
    color: "#7A786F",
    marginBottom: 12,
    display: "block",
  },
  highlightItem: {
    fontSize: 11,
    color: "#5A5850",
    lineHeight: 1.6,
    paddingLeft: 12,
    borderLeft: "2px solid #EA5E33",
    marginBottom: 10,
  },
  notebookRow: {
    display: "flex",
    gap: 12,
    alignItems: "center",
    marginTop: 24,
  },
  notebookLink: {
    display: "inline-block",
    padding: "8px 14px",
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 10,
    fontWeight: 500,
    letterSpacing: "0.3px",
    color: "#EA5E33",
    border: "1px solid #EA5E33",
    borderRadius: 2,
    textDecoration: "none",
    textTransform: "uppercase" as const,
  },
  notebookDownload: {
    display: "inline-block",
    padding: "8px 14px",
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 10,
    fontWeight: 500,
    letterSpacing: "0.3px",
    color: "#7A786F",
    border: "1px solid #C2C0B5",
    borderRadius: 2,
    textDecoration: "none",
    textTransform: "uppercase" as const,
  },
  downloadBtn: {
    display: "inline-block",
    padding: "8px 14px",
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 10,
    fontWeight: 500,
    letterSpacing: "0.3px",
    color: "#fff",
    backgroundColor: "#EA5E33",
    border: "1px solid #EA5E33",
    borderRadius: 2,
    textTransform: "uppercase" as const,
    cursor: "pointer",
  },
  empty: {
    textAlign: "center" as const,
    padding: 64,
    color: "#7A786F",
    fontSize: 11,
    fontFamily: "'JetBrains Mono', monospace",
  },
};

function Crosshair({ style }: { style: React.CSSProperties }) {
  return (
    <div
      style={{
        position: "absolute",
        width: 10,
        height: 10,
        pointerEvents: "none",
        zIndex: 2,
        ...style,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "50%",
          left: 0,
          width: "100%",
          height: 1,
          backgroundColor: "#C2C0B5",
          transform: "translateY(-50%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 0,
          height: "100%",
          width: 1,
          backgroundColor: "#C2C0B5",
          transform: "translateX(-50%)",
        }}
      />
    </div>
  );
}

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

export default function VizDetail() {
  const mobile = useIsMobile();
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useApi<VizDetailData>(
    `/visualizations/${id}`
  );

  if (loading) return <div style={styles.empty}>Loading...</div>;
  if (error) return <div style={styles.empty}>Error: {error}</div>;
  if (!data) return <div style={styles.empty}>Not found</div>;

  return (
    <div style={{
      ...styles.container,
      padding: mobile ? "20px 16px" : "32px 40px",
    }}>
      <Link to="/gallery" style={styles.backLink}>
        {"<-"} Back to Gallery
      </Link>
      <h1 style={styles.title}>{data.title}</h1>
      <p style={styles.desc}>{data.description}</p>

      <div style={{
        ...styles.meta,
        flexWrap: "wrap" as const,
        gap: mobile ? 16 : 32,
      }}>
        <div>
          <div style={styles.metaLabel}>Chart Type</div>
          <div style={styles.metaValue}>{data.chartType}</div>
        </div>
        <div>
          <div style={styles.metaLabel}>Datasets</div>
          <div style={styles.metaValue}>{data.datasetIds.join(", ")}</div>
        </div>
        <div>
          <div style={styles.metaLabel}>Created</div>
          <div style={styles.metaValue}>
            {new Date(data.createdAt).toLocaleDateString()}
          </div>
        </div>
      </div>

      <div style={styles.chartFrame}>
        <Crosshair style={{ top: 0, left: 0 }} />
        <Crosshair style={{ top: 0, right: 0 }} />
        <Crosshair style={{ bottom: 0, left: 0 }} />
        <Crosshair style={{ bottom: 0, right: 0 }} />
        <ChartRenderer html={data.htmlCode} height={520} />
      </div>

      {data.highlights.length > 0 && (
        <div>
          <span style={styles.sectionLabel}>Key Insights</span>
          {data.highlights.map((h, i) => (
            <div key={i} style={styles.highlightItem}>
              {h}
            </div>
          ))}
        </div>
      )}

      <div style={{
        ...styles.notebookRow,
        flexWrap: "wrap" as const,
      }}>
        <button
          onClick={() => downloadHtml(data.htmlCode, `${data.id}.html`)}
          style={styles.downloadBtn}
        >
          Download Chart (.html)
        </button>
        {data.notebookPath && (
          <>
            <a
              href={`/wasm-notebooks/${data.id}.html`}
              target="_blank"
              rel="noopener noreferrer"
              style={styles.notebookLink}
            >
              Open Marimo Notebook (WASM)
            </a>
            <a
              href={`/api/visualizations/${data.id}/notebook`}
              target="_blank"
              rel="noopener noreferrer"
              style={styles.notebookDownload}
            >
              Download .py
            </a>
          </>
        )}
      </div>
    </div>
  );
}
