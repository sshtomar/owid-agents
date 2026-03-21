import { NavLink } from "react-router-dom";
import React from "react";
import { useIsMobile } from "../hooks/useIsMobile";

const baseStyles: Record<string, React.CSSProperties> = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "12px 40px",
    backgroundColor: "#F6F5EE",
    borderBottom: "1px solid #C2C0B5",
    height: 48,
    flexShrink: 0,
  },
  logo: {
    fontSize: 13,
    fontWeight: 600,
    letterSpacing: "0.5px",
    color: "#2B2A27",
    textTransform: "uppercase" as const,
  },
  nav: {
    display: "flex",
    gap: 20,
  },
};

const linkStyle = ({
  isActive,
}: {
  isActive: boolean;
}): React.CSSProperties => ({
  textDecoration: "none",
  color: isActive ? "#EA5E33" : "#7A786F",
  fontWeight: 500,
  fontSize: 11,
  fontFamily: "'JetBrains Mono', monospace",
  letterSpacing: "0.3px",
  textTransform: "uppercase",
});

export default function Header() {
  const mobile = useIsMobile();
  const styles = {
    ...baseStyles,
    header: {
      ...baseStyles.header,
      padding: mobile ? "12px 16px" : "12px 40px",
    },
    nav: {
      ...baseStyles.nav,
      gap: mobile ? 12 : 20,
    },
  };
  return (
    <header style={styles.header}>
      <NavLink to="/" style={{ ...baseStyles.logo, textDecoration: "none" }}>
        Fieldnotes
      </NavLink>
      <nav style={styles.nav}>
        <NavLink to="/gallery" style={linkStyle}>
          Gallery
        </NavLink>
        <NavLink to="/datasets" style={linkStyle}>
          Datasets
        </NavLink>
      </nav>
    </header>
  );
}
