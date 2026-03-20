import React, { useEffect, useRef, useState } from "react";

interface Props {
  html: string;
  height?: number;
}

export default function ChartRenderer({ html, height = 420 }: Props) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [autoHeight, setAutoHeight] = useState(height);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const onLoad = () => {
      try {
        const doc = iframe.contentDocument;
        if (!doc) return;
        const measure = () => {
          const h = doc.documentElement.scrollHeight;
          if (h > 0) setAutoHeight(h);
        };
        measure();
        // Re-measure after fonts and images settle
        setTimeout(measure, 200);
        setTimeout(measure, 600);
      } catch {
        // sandbox may block access in some cases
      }
    };

    iframe.addEventListener("load", onLoad);
    return () => iframe.removeEventListener("load", onLoad);
  }, [html]);

  return (
    <iframe
      ref={iframeRef}
      srcDoc={html}
      sandbox="allow-scripts allow-same-origin"
      style={{
        width: "100%",
        height: autoHeight,
        border: "none",
        borderRadius: 2,
        background: "#F6F5EE",
      }}
      title="Visualization"
    />
  );
}
