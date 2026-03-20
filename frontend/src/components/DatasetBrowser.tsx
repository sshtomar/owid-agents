import React from "react";
import { useApi } from "../hooks/useApi";

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

const styles: Record<string, React.CSSProperties> = {
  container: {
    padding: 32,
  },
  header: {
    marginBottom: 32,
  },
  breadcrumb: {
    color: "#2563eb",
    marginBottom: 8,
    fontSize: 12,
    fontWeight: 600,
    letterSpacing: "0.02em",
  },
  title: {
    fontSize: 24,
    fontWeight: 700,
    letterSpacing: "-0.03em",
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 13,
    color: "#64748b",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse" as const,
    fontSize: 13,
  },
  th: {
    textAlign: "left" as const,
    padding: "10px 16px",
    borderBottom: "2px solid #0f172a",
    fontSize: 11,
    fontWeight: 700,
    textTransform: "uppercase" as const,
    letterSpacing: "0.04em",
    color: "#64748b",
  },
  td: {
    padding: "12px 16px",
    borderBottom: "1px solid #e2e8f0",
    verticalAlign: "top" as const,
  },
  providerBadge: {
    display: "inline-block",
    fontSize: 11,
    fontWeight: 600,
    padding: "2px 8px",
    borderRadius: 4,
    background: "#f1f5f9",
    color: "#475569",
  },
  topicChip: {
    display: "inline-block",
    fontSize: 11,
    fontWeight: 500,
    padding: "1px 6px",
    borderRadius: 3,
    background: "#eff6ff",
    color: "#2563eb",
    marginRight: 4,
    marginBottom: 2,
  },
  link: {
    color: "#2563eb",
    textDecoration: "none",
    fontSize: 11,
  },
  empty: {
    textAlign: "center" as const,
    padding: 64,
    color: "#94a3b8",
  },
};

export default function DatasetBrowser() {
  const { data, loading, error } = useApi<DatasetsResponse>("/datasets");

  if (loading) return <div style={styles.empty}>Loading datasets...</div>;
  if (error) return <div style={styles.empty}>Failed to load: {error}</div>;

  const datasets = data?.datasets ?? [];

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.breadcrumb}>Data Catalog</div>
        <h1 style={styles.title}>Discovered Datasets</h1>
        <p style={styles.subtitle}>
          {datasets.length} dataset{datasets.length !== 1 ? "s" : ""} from World
          Bank and WHO
        </p>
      </div>

      {datasets.length === 0 ? (
        <div style={styles.empty}>
          No datasets yet. Run the discovery agent to find some.
        </div>
      ) : (
        <table style={styles.table}>
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
                  <div style={{ fontWeight: 600 }}>{ds.title}</div>
                  <div style={{ fontSize: 11, color: "#94a3b8", marginTop: 2 }}>
                    {ds.id}
                  </div>
                </td>
                <td style={styles.td}>
                  <span style={styles.providerBadge}>
                    {ds.source.provider === "world-bank" ? "World Bank" : "WHO"}
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
      )}
    </div>
  );
}
