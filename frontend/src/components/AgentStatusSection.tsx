import React, { useEffect, useState, useMemo } from "react";
import { motion } from "framer-motion";
import SidebarSection from "./SidebarSection";
import { COLORS, FONTS } from "../theme";

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

export default function AgentStatusSection({ delay }: { delay: number }) {
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
              backgroundColor: COLORS.accent,
              flexShrink: 0,
            }}
          />
          <span style={{
            fontFamily: FONTS.mono,
            fontSize: 10,
            fontWeight: 500,
            color: COLORS.text,
          }}>
            Running
          </span>
        </div>
        <span style={{
          fontFamily: FONTS.mono,
          fontSize: 9,
          color: COLORS.textMuted,
        }}>
          v1.0.0
        </span>
      </div>
      <div style={{
        fontSize: 11,
        color: COLORS.textMuted,
        lineHeight: 1.5,
        minHeight: 34,
        transition: "opacity 0.4s ease",
        opacity: visible ? 1 : 0,
      }}>
        {AGENT_ACTIVITIES[activityIndex]}
      </div>
      <div style={{
        marginTop: 8,
        fontFamily: FONTS.mono,
        fontSize: 9,
        color: COLORS.textSubtle,
      }}>
        {elapsed}
      </div>
    </SidebarSection>
  );
}
