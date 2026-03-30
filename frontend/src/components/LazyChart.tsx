import React, { useRef, useState, useEffect } from "react";
import { useInView } from "framer-motion";
import ChartRenderer from "./ChartRenderer";
import { COLORS, FONTS } from "../theme";

interface LazyChartProps {
  vizId: string;
  height?: number;
  hideChrome?: boolean;
}

export default function LazyChart({ vizId, height = 420, hideChrome = false }: LazyChartProps) {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, margin: "200px" });
  const [html, setHtml] = useState<string | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!isInView || html) return;
    let cancelled = false;
    fetch(`/api/visualizations/${vizId}`)
      .then((res) => {
        if (!res.ok) throw new Error(`${res.status}`);
        return res.json();
      })
      .then((data: { htmlCode?: string }) => {
        if (!cancelled && data.htmlCode) {
          setHtml(data.htmlCode);
        }
      })
      .catch(() => {
        if (!cancelled) setError(true);
      });
    return () => { cancelled = true; };
  }, [isInView, vizId, html]);

  return (
    <div ref={ref} style={{ minHeight: hideChrome ? 300 : height }}>
      {html ? (
        <ChartRenderer html={html} height={height} hideChrome={hideChrome} />
      ) : error ? (
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: 200,
          color: COLORS.textMuted,
          fontFamily: FONTS.mono,
          fontSize: 10,
        }}>
          Failed to load chart
        </div>
      ) : isInView ? (
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: 200,
          color: COLORS.textSubtle,
          fontFamily: FONTS.mono,
          fontSize: 10,
        }}>
          Loading chart...
        </div>
      ) : null}
    </div>
  );
}
