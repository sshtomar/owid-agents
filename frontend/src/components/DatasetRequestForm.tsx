import React, { useState, useEffect } from "react";
import SidebarSection from "./SidebarSection";
import { postApi } from "../hooks/useApi";
import { COLORS, FONTS, BUTTON_PRIMARY } from "../theme";
import { trackDatasetRequest } from "../analytics";

interface DatasetRequest {
  id: string;
  topic: string;
  description?: string;
  name?: string;
  createdAt: string;
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  fontFamily: FONTS.mono,
  fontSize: 10,
  padding: "6px 8px",
  border: `1px solid ${COLORS.borderStrong}`,
  borderRadius: 2,
  backgroundColor: COLORS.white,
  color: COLORS.text,
  outline: "none",
  boxSizing: "border-box",
};

export default function DatasetRequestForm({ delay }: { delay: number }) {
  const [topic, setTopic] = useState("");
  const [description, setDescription] = useState("");
  const [name, setName] = useState("");
  const [sent, setSent] = useState(false);
  const [recentRequests, setRecentRequests] = useState<DatasetRequest[]>([]);

  useEffect(() => {
    fetch("/api/requests")
      .then((r) => r.json())
      .then((data: { requests: DatasetRequest[] }) =>
        setRecentRequests(data.requests.slice(-5).reverse()),
      )
      .catch(() => {});
  }, []);

  const handleSubmit = async () => {
    if (!topic.trim()) return;
    try {
      const entry = await postApi<DatasetRequest>("/requests", {
        topic: topic.trim(),
        description: description.trim() || undefined,
        name: name.trim() || undefined,
      });
      trackDatasetRequest(topic.trim());
      setTopic("");
      setDescription("");
      setName("");
      setSent(true);
      setRecentRequests((prev) => [entry, ...prev].slice(0, 5));
      setTimeout(() => setSent(false), 2000);
    } catch {
      // postApi throws on non-200, user sees no change
    }
  };

  return (
    <SidebarSection label="Request a dataset" delay={delay}>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        <input
          type="text"
          placeholder="Topic (e.g. deforestation)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          maxLength={200}
          style={inputStyle}
        />
        <textarea
          placeholder="Details (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={2}
          maxLength={1000}
          style={{ ...inputStyle, resize: "vertical" }}
        />
        <input
          type="text"
          placeholder="Your name (optional)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          maxLength={100}
          style={inputStyle}
        />
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <button onClick={handleSubmit} style={BUTTON_PRIMARY}>
            Submit
          </button>
          {sent && (
            <span style={{ fontFamily: FONTS.mono, fontSize: 10, color: COLORS.textMuted }}>
              Sent!
            </span>
          )}
        </div>
      </div>
      {recentRequests.length > 0 && (
        <div style={{ marginTop: 14 }}>
          <div style={{
            fontSize: 9,
            textTransform: "uppercase",
            letterSpacing: "0.5px",
            color: COLORS.textSubtle,
            marginBottom: 6,
            fontFamily: FONTS.mono,
          }}>
            Recent requests
          </div>
          {recentRequests.map((r) => (
            <div
              key={r.id}
              style={{
                fontSize: 11,
                color: COLORS.textMid,
                lineHeight: 1.5,
                paddingLeft: 10,
                borderLeft: `2px solid ${COLORS.border}`,
                marginBottom: 6,
              }}
            >
              {r.topic}
              {r.name && (
                <span style={{ color: COLORS.textSubtle }}> -- {r.name}</span>
              )}
            </div>
          ))}
        </div>
      )}
    </SidebarSection>
  );
}
