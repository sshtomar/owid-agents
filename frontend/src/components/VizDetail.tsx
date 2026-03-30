import React, { useState, useEffect, useCallback, useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import { useApi, postApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";
import ChartRenderer from "./ChartRenderer";
import ErrorBoundary from "./ErrorBoundary";
import {
  COLORS, FONTS,
  BUTTON_PRIMARY, BUTTON_SECONDARY, BUTTON_ACCENT_OUTLINE,
  LABEL_STYLE, relativeTime,
} from "../theme";
import { VizMeta, VizListResponse, findRelated } from "../search";
import {
  trackReaction, trackComment, trackDownload, trackCopy,
  trackNotebookOpened, trackRelatedChartClicked,
} from "../analytics";

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

function Crosshair({ style }: { style: React.CSSProperties }) {
  return (
    <div style={{
      position: "absolute",
      width: 10,
      height: 10,
      pointerEvents: "none",
      zIndex: 2,
      ...style,
    }}>
      <div style={{
        position: "absolute",
        top: "50%",
        left: 0,
        width: "100%",
        height: 1,
        backgroundColor: COLORS.borderStrong,
        transform: "translateY(-50%)",
      }} />
      <div style={{
        position: "absolute",
        left: "50%",
        top: 0,
        height: "100%",
        width: 1,
        backgroundColor: COLORS.borderStrong,
        transform: "translateX(-50%)",
      }} />
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
      trackReaction(vizId, reaction);
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
    try {
      await postApi("/feedback", {
        vizId,
        reaction: selected ?? "useful",
        comment: comment.trim(),
      });
      trackComment(vizId);
      setComment("");
      setCommentSent(true);
      setTimeout(() => setCommentSent(false), 2000);
    } catch {
      // silent -- user sees no change
    }
  }, [vizId, selected, comment]);

  return (
    <div style={{ marginTop: 28, marginBottom: 24 }}>
      <span style={{ ...LABEL_STYLE, marginBottom: 10, display: "block" }}>
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
                ...BUTTON_SECONDARY,
                gap: 6,
                color: isSelected ? COLORS.white : COLORS.textMuted,
                backgroundColor: isSelected ? COLORS.accent : "transparent",
                borderColor: isSelected ? COLORS.accent : COLORS.borderStrong,
                cursor: selected && !isSelected ? "default" : "pointer",
                opacity: selected && !isSelected ? 0.5 : 1,
              }}
            >
              {label}
              {counts[key] > 0 && (
                <span style={{ fontSize: 9, opacity: 0.8, fontWeight: 400 }}>
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
              fontFamily: FONTS.mono,
              fontSize: 10,
              color: COLORS.textMuted,
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
              maxLength={1000}
              style={{
                fontFamily: FONTS.mono,
                fontSize: 11,
                padding: "8px 10px",
                border: `1px solid ${COLORS.borderStrong}`,
                borderRadius: 2,
                backgroundColor: COLORS.white,
                color: COLORS.text,
                resize: "vertical",
                outline: "none",
              }}
            />
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              <button onClick={handleComment} style={BUTTON_PRIMARY}>
                Send
              </button>
              {commentSent && (
                <span style={{ fontFamily: FONTS.mono, fontSize: 10, color: COLORS.textMuted }}>
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

function EmbedBlock({ vizId, title }: { vizId: string; title: string }) {
  const [copied, setCopied] = useState<"embed" | "share" | null>(null);
  const embedUrl = `${window.location.origin}/embed/${vizId}`;
  const shareUrl = `${window.location.origin}/share/${vizId}`;
  const iframeCode = `<iframe src="${embedUrl}" loading="lazy" style="width: 100%; height: 600px; border: 0px none;" allow="web-share"></iframe>`;

  const copyText = (text: string, type: "embed" | "share") => {
    navigator.clipboard.writeText(text).then(() => {
      trackCopy(vizId, type);
      setCopied(type);
      setTimeout(() => setCopied(null), 2000);
    });
  };

  const codeBlock: React.CSSProperties = {
    fontFamily: FONTS.mono,
    fontSize: 10,
    lineHeight: 1.6,
    color: COLORS.textMid,
    backgroundColor: COLORS.inputBg,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 2,
    padding: "10px 12px",
    whiteSpace: "pre-wrap",
    wordBreak: "break-all",
    userSelect: "all",
  };

  const copyBtn: React.CSSProperties = {
    ...BUTTON_SECONDARY,
    fontSize: 9,
    padding: "3px 8px",
    marginTop: 6,
  };

  return (
    <div style={{ marginTop: 32, borderTop: `1px solid ${COLORS.border}`, paddingTop: 24 }}>
      <span style={{ ...LABEL_STYLE, marginBottom: 16, display: "block" }}>
        Share & Embed
      </span>

      <div style={{ marginBottom: 16 }}>
        <span style={{ ...LABEL_STYLE, fontSize: 8, marginBottom: 6, display: "block" }}>
          Share link (with preview)
        </span>
        <p style={{ fontSize: 11, color: COLORS.textMuted, lineHeight: 1.6, marginTop: 0, marginBottom: 8 }}>
          Paste this link on social media, Slack, or Notion for a rich preview.
        </p>
        <div style={codeBlock}>{shareUrl}</div>
        <button onClick={() => copyText(shareUrl, "share")} style={copyBtn}>
          {copied === "share" ? "Copied" : "Copy share link"}
        </button>
      </div>

      <div>
        <span style={{ ...LABEL_STYLE, fontSize: 8, marginBottom: 6, display: "block" }}>
          Embed code
        </span>
        <p style={{ fontSize: 11, color: COLORS.textMuted, lineHeight: 1.6, marginTop: 0, marginBottom: 8 }}>
          Paste this into any webpage. The chart is interactive and self-contained.
        </p>
        <div style={codeBlock}>{iframeCode}</div>
        <button onClick={() => copyText(iframeCode, "embed")} style={copyBtn}>
          {copied === "embed" ? "Copied" : "Copy embed code"}
        </button>
      </div>
    </div>
  );
}

function CitationBlock({ viz }: { viz: VizDetailData }) {
  const [copied, setCopied] = useState<"cite" | "bibtex" | null>(null);
  const year = new Date(viz.createdAt).getFullYear();
  const dateStr = new Date(viz.createdAt).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
  const slug = viz.title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
  const url = `${window.location.origin}/viz/${viz.id}`;

  const citeText =
    `OWID Agents (${year}) - "${viz.title}". ` +
    `Published online at OWIDAgents. Retrieved from: '${url}' [Online Resource].`;

  const bibtex =
    `@article{owid-agents-${slug},\n` +
    `    author = {OWID Agents},\n` +
    `    title = {${viz.title}},\n` +
    `    journal = {OWID Agents},\n` +
    `    year = {${year}},\n` +
    `    note = {${url}}\n` +
    `}`;

  const copyToClipboard = (text: string, type: "cite" | "bibtex") => {
    navigator.clipboard.writeText(text).then(() => {
      trackCopy(viz.id, type === "cite" ? "citation" : "bibtex");
      setCopied(type);
      setTimeout(() => setCopied(null), 2000);
    });
  };

  const sectionLabel: React.CSSProperties = {
    ...LABEL_STYLE,
    marginBottom: 8,
    display: "block",
  };

  const codeBlock: React.CSSProperties = {
    fontFamily: FONTS.mono,
    fontSize: 10,
    lineHeight: 1.6,
    color: COLORS.textMid,
    backgroundColor: COLORS.inputBg,
    border: `1px solid ${COLORS.border}`,
    borderRadius: 2,
    padding: "10px 12px",
    whiteSpace: "pre-wrap",
    wordBreak: "break-word",
    position: "relative",
  };

  const copyBtn: React.CSSProperties = {
    ...BUTTON_SECONDARY,
    fontSize: 9,
    padding: "3px 8px",
    marginTop: 6,
  };

  return (
    <div style={{ marginTop: 32, borderTop: `1px solid ${COLORS.border}`, paddingTop: 24 }}>
      <span style={{ ...LABEL_STYLE, marginBottom: 16, display: "block" }}>
        Cite this work
      </span>
      <p style={{ fontSize: 11, color: COLORS.textMuted, lineHeight: 1.6, marginTop: 0, marginBottom: 16 }}>
        Our visualizations rely on work from many different people and organizations.
        When citing this visualization, please also cite the underlying data sources.
      </p>

      <div style={{ marginBottom: 16 }}>
        <span style={sectionLabel}>Citation</span>
        <div style={codeBlock}>{citeText}</div>
        <button style={copyBtn} onClick={() => copyToClipboard(citeText, "cite")}>
          {copied === "cite" ? "Copied" : "Copy citation"}
        </button>
      </div>

      <div>
        <span style={sectionLabel}>BibTeX</span>
        <div style={codeBlock}>{bibtex}</div>
        <button style={copyBtn} onClick={() => copyToClipboard(bibtex, "bibtex")}>
          {copied === "bibtex" ? "Copied" : "Copy BibTeX"}
        </button>
      </div>
    </div>
  );
}

function RelatedCharts({ current, allViz }: { current: VizMeta; allViz: VizMeta[] }) {
  const related = useMemo(() => findRelated(current, allViz, 3), [current, allViz]);

  if (related.length === 0) return null;

  return (
    <div style={{ marginTop: 32 }}>
      <span style={{ ...LABEL_STYLE, marginBottom: 16, display: "block" }}>
        Related Charts
      </span>
      <div style={{ display: "flex", gap: 16, flexWrap: "wrap" }}>
        {related.map((viz) => (
          <Link
            key={viz.id}
            to={`/viz/${viz.id}`}
            onClick={() => trackRelatedChartClicked(current.id, viz.id, viz.title)}
            style={{
              textDecoration: "none",
              color: "inherit",
              flex: "1 1 200px",
              maxWidth: 280,
              padding: 12,
              border: `1px solid ${COLORS.border}`,
              borderRadius: 2,
              backgroundColor: COLORS.bg,
            }}
          >
            <div style={{
              fontSize: 12,
              fontWeight: 600,
              color: COLORS.text,
              marginBottom: 4,
              letterSpacing: "-0.2px",
            }}>
              {viz.title}
            </div>
            <div style={{
              fontSize: 10,
              color: COLORS.textMuted,
              lineHeight: 1.5,
            }}>
              {viz.description.split(".")[0]}.
            </div>
            <div style={{
              fontSize: 8,
              fontFamily: FONTS.mono,
              color: COLORS.textSubtle,
              marginTop: 6,
              textTransform: "uppercase",
            }}>
              {viz.chartType}
            </div>
          </Link>
        ))}
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

const emptyStyle: React.CSSProperties = {
  textAlign: "center",
  padding: 64,
  color: COLORS.textMuted,
  fontSize: 11,
  fontFamily: FONTS.mono,
};

export default function VizDetail() {
  const mobile = useIsMobile();
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useApi<VizDetailData>(`/visualizations/${id}`);
  const allVizResp = useApi<VizListResponse>("/visualizations");

  if (loading) return <div style={emptyStyle}>Loading...</div>;
  if (error) return <div style={emptyStyle}>Error: {error}</div>;
  if (!data) return <div style={emptyStyle}>Not found</div>;

  const allViz = allVizResp.data?.visualizations ?? [];
  const currentMeta: VizMeta = {
    id: data.id,
    title: data.title,
    description: data.description,
    chartType: data.chartType,
    highlights: data.highlights,
    createdAt: data.createdAt,
    datasetIds: data.datasetIds,
    codeFilePath: "",
    notebookPath: data.notebookPath,
  };

  return (
    <div style={{
      padding: mobile ? "20px 16px" : "32px 40px",
      maxWidth: 960,
      backgroundColor: COLORS.bg,
      minHeight: "100%",
    }}>
      <Link to="/gallery" style={{
        fontFamily: FONTS.mono,
        fontSize: 10,
        color: COLORS.accent,
        textDecoration: "none",
        letterSpacing: "0.3px",
        display: "inline-block",
        marginBottom: 20,
      }}>
        {"<-"} Back to Gallery
      </Link>
      <h1 style={{
        fontSize: 18,
        fontWeight: 600,
        letterSpacing: "-0.3px",
        color: COLORS.text,
        marginBottom: 6,
      }}>
        {data.title}
      </h1>
      <p style={{
        fontSize: 11,
        color: COLORS.textMuted,
        lineHeight: 1.6,
        marginBottom: 24,
        maxWidth: 600,
      }}>
        {data.description}
      </p>

      <div style={{
        display: "flex",
        gap: mobile ? 16 : 32,
        marginBottom: 24,
        borderBottom: `1px solid ${COLORS.borderStrong}`,
        paddingBottom: 16,
        flexWrap: "wrap",
      }}>
        <div>
          <div style={LABEL_STYLE}>Chart Type</div>
          <div style={{ fontSize: 11, fontWeight: 500, color: COLORS.text }}>{data.chartType}</div>
        </div>
        <div>
          <div style={LABEL_STYLE}>Datasets</div>
          <div style={{ fontSize: 11, fontWeight: 500, color: COLORS.text }}>{data.datasetIds.join(", ")}</div>
        </div>
        <div>
          <div style={LABEL_STYLE}>Created</div>
          <div style={{ fontSize: 11, fontWeight: 500, color: COLORS.text }}>
            {new Date(data.createdAt).toLocaleDateString()}
            <span style={{ color: COLORS.textSubtle, fontWeight: 400, marginLeft: 6, fontSize: 9 }}>
              ({relativeTime(data.createdAt)})
            </span>
          </div>
        </div>
      </div>

      <div style={{
        border: `1px solid ${COLORS.border}`,
        borderRadius: 2,
        overflow: "hidden",
        marginBottom: 24,
        position: "relative",
      }}>
        <Crosshair style={{ top: 0, left: 0 }} />
        <Crosshair style={{ top: 0, right: 0 }} />
        <Crosshair style={{ bottom: 0, left: 0 }} />
        <Crosshair style={{ bottom: 0, right: 0 }} />
        <ErrorBoundary>
          <ChartRenderer html={data.htmlCode} height={520} />
        </ErrorBoundary>
      </div>

      {data.highlights.length > 0 && (
        <div>
          <span style={{ ...LABEL_STYLE, marginBottom: 12, display: "block" }}>Key Insights</span>
          {data.highlights.map((h, i) => (
            <div key={i} style={{
              fontSize: 11,
              color: COLORS.textMid,
              lineHeight: 1.6,
              paddingLeft: 12,
              borderLeft: `2px solid ${COLORS.accent}`,
              marginBottom: 10,
            }}>
              {h}
            </div>
          ))}
        </div>
      )}

      <ReactionBar vizId={data.id} />

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 24 }}>
        <button
          onClick={() => { trackDownload(data.id, "html"); downloadHtml(data.htmlCode, `${data.id}.html`); }}
          style={BUTTON_PRIMARY}
        >
          Download Chart (.html)
        </button>
        {data.notebookPath && (
          <>
            <a
              href={`/wasm-notebooks/${data.id}.html`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ ...BUTTON_ACCENT_OUTLINE, textDecoration: "none" }}
              onClick={() => trackNotebookOpened(data.id)}
            >
              Open Marimo Notebook (WASM)
            </a>
            <a
              href={`/api/visualizations/${data.id}/notebook`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ ...BUTTON_SECONDARY, textDecoration: "none" }}
              onClick={() => trackDownload(data.id, "py")}
            >
              Download .py
            </a>
          </>
        )}
      </div>

      <EmbedBlock vizId={data.id} title={data.title} />

      <CitationBlock viz={data} />

      <RelatedCharts current={currentMeta} allViz={allViz} />
    </div>
  );
}
