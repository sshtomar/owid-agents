import React, { useEffect } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import Header from "./components/Header";
import Landing from "./components/Landing";
import VizGallery from "./components/VizGallery";
import VizDetail from "./components/VizDetail";
import DatasetBrowser from "./components/DatasetBrowser";
import { initPostHog, capturePageView } from "./analytics";

initPostHog();

const styles: Record<string, React.CSSProperties> = {
  app: {
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
    backgroundColor: "#F6F5EE",
  },
  content: {
    flex: 1,
    overflow: "auto",
    backgroundColor: "#F6F5EE",
  },
  contentFull: {
    flex: 1,
    overflow: "auto",
  },
};

export default function App() {
  const location = useLocation();
  const isLanding = location.pathname === "/";

  useEffect(() => {
    capturePageView(location.pathname);
  }, [location.pathname]);

  return (
    <div style={styles.app}>
      {!isLanding && <Header />}
      <main style={isLanding ? styles.contentFull : styles.content}>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/gallery" element={<VizGallery />} />
          <Route path="/viz/:id" element={<VizDetail />} />
          <Route path="/datasets" element={<DatasetBrowser />} />
        </Routes>
      </main>
    </div>
  );
}
