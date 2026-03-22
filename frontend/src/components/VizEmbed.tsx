import { useParams } from "react-router-dom";
import { useApi } from "../hooks/useApi";
import ChartRenderer from "./ChartRenderer";

interface VizEmbedData {
  id: string;
  title: string;
  htmlCode: string;
}

export default function VizEmbed() {
  const { id } = useParams<{ id: string }>();
  const { data, loading, error } = useApi<VizEmbedData>(`/visualizations/${id}`);

  if (loading) return <div style={{ padding: 20, fontFamily: "sans-serif", fontSize: 12, color: "#888" }}>Loading...</div>;
  if (error || !data) return <div style={{ padding: 20, fontFamily: "sans-serif", fontSize: 12, color: "#888" }}>Chart not found</div>;

  return (
    <div style={{ width: "100%", height: "100vh", overflow: "hidden" }}>
      <ChartRenderer html={data.htmlCode} />
    </div>
  );
}
