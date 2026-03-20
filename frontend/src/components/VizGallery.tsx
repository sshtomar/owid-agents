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
  createdAt: string;
  generatedCode: string;
}

interface VizListResponse {
  visualizations: VizEntry[];
  count: number;
}

const SPRING = {
  gentle: { type: "spring" as const, stiffness: 300, damping: 30 },
};

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
          <ChartRenderer html={viz.generatedCode} />
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
    </motion.div>
  );
}

export default function VizGallery() {
  const { data, loading, error } = useApi<VizListResponse>("/visualizations");

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

  const vizList = data?.visualizations ?? [];

  return (
    <div style={{
      padding: "32px 40px",
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
        <p style={{ fontSize: 12, color: "#7A786F" }}>
          {vizList.length} visualizations from public datasets
        </p>
      </div>

      {vizList.length === 0 ? (
        <div style={{
          textAlign: "center",
          padding: 64,
          color: "#7A786F",
          fontSize: 11,
          fontFamily: "'JetBrains Mono', monospace",
        }}>
          No visualizations yet.
        </div>
      ) : (
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(500px, 1fr))",
          gap: 40,
        }}>
          {vizList.map((viz, i) => (
            <GalleryCard key={viz.id} viz={viz} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}
