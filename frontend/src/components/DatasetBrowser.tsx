import React from "react";
import { useApi } from "../hooks/useApi";
import { useIsMobile } from "../hooks/useIsMobile";

interface DatasetEntry {
  id: string;
  title: string;
  description: string;
  source: {
    provider: string;
    indicatorId: string;
    sourceUrl: string;
    lastFetched: string;
  };
  topics: string[];
  countries: string[];
  dateRange: { start: string; end: string };
  dataPointCount: number;
}

interface DatasetsResponse {
  datasets: DatasetEntry[];
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

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: 32,
    backgroundColor: "#F6F5EE",
    minHeight: "100%",
  },
  header: {
    marginBottom: 32,
  },
  breadcrumb: {
    color: "#EA5E33",
    marginBottom: 8,
    fontSize: 10,
    fontWeight: 500,
    letterSpacing: "0.3px",
    fontFamily: "'JetBrains Mono', monospace",
    textTransform: "uppercase" as const,
  },
  title: {
    fontSize: 24,
    fontWeight: 700,
    letterSpacing: "-0.03em",
    marginBottom: 8,
    color: "#2B2A27",
  },
  subtitle: {
    fontSize: 13,
    color: "#7A786F",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse" as const,
    fontSize: 13,
  },
  th: {
    textAlign: "left" as const,
    padding: "10px 16px",
    borderBottom: "2px solid #94918A",
    fontSize: 11,
    fontWeight: 700,
    textTransform: "uppercase" as const,
    letterSpacing: "0.04em",
    color: "#7A786F",
    fontFamily: "'JetBrains Mono', monospace",
  },
  td: {
    padding: "12px 16px",
    borderBottom: "1px solid #E2E0D5",
    verticalAlign: "top" as const,
    color: "#2B2A27",
  },
  providerBadge: {
    display: "inline-block",
    fontSize: 11,
    fontWeight: 600,
    padding: "2px 8px",
    borderRadius: 4,
    background: "#EEEDE6",
    color: "#5A5850",
  },
  topicChip: {
    display: "inline-block",
    fontSize: 11,
    fontWeight: 500,
    padding: "1px 6px",
    borderRadius: 3,
    background: "#EEEDE6",
    color: "#8B7355",
    marginRight: 4,
    marginBottom: 2,
  },
  link: {
    color: "#EA5E33",
    textDecoration: "none",
    fontSize: 11,
  },
  empty: {
    textAlign: "center" as const,
    padding: 64,
    color: "#7A786F",
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 11,
  },
};

export default function DatasetBrowser() {
  const mobile = useIsMobile();
  const { data, loading, error } = useApi<DatasetsResponse>("/datasets");

  if (loading) return <div style={styles.empty}>Loading datasets...</div>;
  if (error) return <div style={styles.empty}>Failed to load: {error}</div>;

  const datasets = data?.datasets ?? [];

  return (
    <div style={{
      ...styles.container,
      padding: mobile ? 16 : 32,
    }}>
      <div style={styles.header}>
        <div style={styles.breadcrumb}>Data Catalog</div>
        <h1 style={styles.title}>Discovered Datasets</h1>
        <p style={styles.subtitle}>
          {datasets.length} dataset{datasets.length !== 1 ? "s" : ""} from 8
          providers
        </p>
      </div>

      {datasets.length === 0 ? (
        <div style={styles.empty}>
          No datasets yet. Run the discovery agent to find some.
        </div>
      ) : (
        <div style={{ overflowX: "auto", WebkitOverflowScrolling: "touch" }}>
        <table style={{ ...styles.table, minWidth: 700 }}>
          <thead>
            <tr>
              <th style={styles.th}>Dataset</th>
              <th style={styles.th}>Provider</th>
              <th style={styles.th}>Range</th>
              <th style={styles.th}>Points</th>
              <th style={styles.th}>Topics</th>
              <th style={styles.th}>Source</th>
            </tr>
          </thead>
          <tbody>
            {datasets.map((ds) => (
              <tr key={ds.id}>
                <td style={styles.td}>
                  <div style={{ fontWeight: 600, color: "#2B2A27" }}>{ds.title}</div>
                  <div style={{ fontSize: 11, color: "#94918A", marginTop: 2, fontFamily: "'JetBrains Mono', monospace" }}>
                    {ds.id}
                  </div>
                </td>
                <td style={styles.td}>
                  <span style={styles.providerBadge}>
                    {PROVIDER_LABELS[ds.source.provider] ?? ds.source.provider}
                  </span>
                </td>
                <td style={styles.td}>
                  {ds.dateRange.start} - {ds.dateRange.end}
                </td>
                <td style={styles.td}>
                  {ds.dataPointCount.toLocaleString()}
                </td>
                <td style={styles.td}>
                  {ds.topics.map((t) => (
                    <span key={t} style={styles.topicChip}>
                      {t}
                    </span>
                  ))}
                </td>
                <td style={styles.td}>
                  <a
                    href={ds.source.sourceUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={styles.link}
                  >
                    View source
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        </div>
      )}
    </div>
  );
}
