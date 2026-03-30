import React from "react";
import { motion } from "framer-motion";
import { COLORS, FONTS, SPRING } from "../theme";

export default function SidebarSection({
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
        borderBottom: `1px solid ${COLORS.border}`,
        paddingBottom: 20,
      }}
    >
      <div style={{
        fontSize: 9,
        textTransform: "uppercase",
        letterSpacing: "0.5px",
        color: COLORS.textMuted,
        marginBottom: 10,
        fontFamily: FONTS.mono,
      }}>
        {label}
      </div>
      {children}
    </motion.div>
  );
}
