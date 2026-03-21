import React, { useState, useEffect, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import { postApi } from "../hooks/useApi";
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

type Reaction = "useful" | "interesting" | "surprising" | "needs-work";

const REACTIONS: { key: Reaction; label: string }[] = [
  { key: "useful", label: "Useful" },
  { key: "interesting", label: "Interesting" },
  { key: "surprising", label: "Surprising" },
  { key: "needs-work", label: "Needs work" },
];

interface FeedbackResponse {
  counts: Record<Reaction, number>;
}

function ReactionBar({ vizId }: { vizId: string }) {
  const [counts, setCounts] = useState<Record<Reaction, number>>({
    useful: 0,
    interesting: 0,
    surprising: 0,
    "needs-work": 0,
  });
  const [selected, setSelected] = useState<Reaction | null>(() => {
    try {
      return localStorage.getItem(`feedback-${vizId}`) as Reaction | null;
    } catch {
      return null;
    }
  });
  const [commentOpen, setCommentOpen] = useState(false);
  const [comment, setComment] = useState("");
  const [commentSent, setCommentSent] = useState(false);

  useEffect(() => {
    fetch(`/api/feedback/${vizId}`)
      .then((r) => r.json())
      .then((data: FeedbackResponse) => setCounts(data.counts))
      .catch(() => {});
  }, [vizId]);

  const handleReaction = useCallback(
    async (reaction: Reaction) => {
      if (selected) return;
      setSelected(reaction);
      try {
        localStorage.setItem(`feedback-${vizId}`, reaction);
      } catch {}
      setCounts((prev) => ({ ...prev, [reaction]: prev[reaction] + 1 }));
      await postApi("/feedback", { vizId, reaction }).catch(() => {});
    },
    [vizId, selected],
  );

  const handleComment = useCallback(async () => {
    if (!comment.trim()) return;
    await postApi("/feedback", {
      vizId,
      reaction: selected ?? "useful",
      comment: comment.trim(),
    }).catch(() => {});
    setComment("");
    setCommentSent(true);
    setTimeout(() => setCommentSent(false), 2000);
  }, [vizId, selected, comment]);

  return (
    <div style={{ marginTop: 28, marginBottom: 24 }}>
      <span
        style={{
          fontSize: 9,
          textTransform: "uppercase",
          fontWeight: 500,
          fontFamily: "'JetBrains Mono', monospace",
          letterSpacing: "0.3px",
          color: "#7A786F",
          marginBottom: 10,
          display: "block",
        }}
      >
        Reactions
      </span>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        {REACTIONS.map(({ key, label }) => {
          const isSelected = selected === key;
          return (
            <button
              key={key}
              onClick={() => handleReaction(key)}
              disabled={!!selected && !isSelected}
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: 6,
                padding: "6px 12px",
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 10,
                fontWeight: 500,
                letterSpacing: "0.3px",
                color: isSelected ? "#fff" : "#7A786F",
                backgroundColor: isSelected ? "#EA5E33" : "transparent",
                border: `1px solid ${isSelected ? "#EA5E33" : "#C2C0B5"}`,
                borderRadius: 2,
                cursor: selected && !isSelected ? "default" : "pointer",
                opacity: selected && !isSelected ? 0.5 : 1,
                textTransform: "uppercase",
              }}
            >
              {label}
              {counts[key] > 0 && (
                <span
                  style={{
                    fontSize: 9,
                    opacity: 0.8,
                    fontWeight: 400,
                  }}
                >
                  {counts[key]}
                </span>
              )}
            </button>
          );
        })}
      </div>
      <div style={{ marginTop: 12 }}>
        {!commentOpen ? (
          <button
            onClick={() => setCommentOpen(true)}
            style={{
              background: "none",
              border: "none",
              padding: 0,
              fontFamily: "'JetBrains Mono', monospace",
              fontSize: 10,
              color: "#7A786F",
              cursor: "pointer",
              letterSpacing: "0.3px",
            }}
          >
            + Leave a comment
          </button>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="What did you think?"
              rows={3}
              style={{
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 11,
                padding: "8px 10px",
                border: "1px solid #C2C0B5",
                borderRadius: 2,
                backgroundColor: "#fff",
                color: "#2B2A27",
                resize: "vertical",
                outline: "none",
              }}
            />
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <button
                onClick={handleComment}
                style={{
                  display: "inline-block",
                  padding: "6px 12px",
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 10,
                  fontWeight: 500,
                  letterSpacing: "0.3px",
                  color: "#fff",
                  backgroundColor: "#EA5E33",
                  border: "1px solid #EA5E33",
                  borderRadius: 2,
                  cursor: "pointer",
                  textTransform: "uppercase",
                }}
              >
                Send
              </button>
              {commentSent && (
                <span
                  style={{
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 10,
                    color: "#7A786F",
                  }}
                >
                  Sent!
                </span>
              )}
            </div>
          </div>
        )}
      </div>
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

      <ReactionBar vizId={data.id} />

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
