import posthog from "posthog-js";

// Centralized analytics events. Every capture goes through here so we get
// consistent naming and typed properties without scattering posthog.capture
// calls across the codebase.

export function trackChartViewed(vizId: string, title: string, chartType: string) {
  posthog.capture("chart_viewed", { viz_id: vizId, title, chart_type: chartType });
}

export function trackChartClicked(vizId: string, title: string, source: string) {
  posthog.capture("chart_clicked", { viz_id: vizId, title, source });
}

export function trackSearch(query: string, resultCount: number, totalCount: number) {
  posthog.capture("search_performed", { query, result_count: resultCount, total_count: totalCount });
}

export function trackThemeFilter(themes: string[], resultCount: number) {
  posthog.capture("theme_filter_changed", { themes, result_count: resultCount });
}

export function trackReaction(vizId: string, reaction: string) {
  posthog.capture("chart_reaction", { viz_id: vizId, reaction });
}

export function trackComment(vizId: string) {
  posthog.capture("chart_comment_submitted", { viz_id: vizId });
}

export function trackDatasetRequest(topic: string) {
  posthog.capture("dataset_requested", { topic });
}

export function trackDownload(vizId: string, format: string) {
  posthog.capture("chart_downloaded", { viz_id: vizId, format });
}

export function trackCopy(vizId: string, contentType: "embed" | "share" | "citation" | "bibtex") {
  posthog.capture("content_copied", { viz_id: vizId, content_type: contentType });
}

export function trackNotebookOpened(vizId: string) {
  posthog.capture("notebook_opened", { viz_id: vizId });
}

export function trackRelatedChartClicked(fromVizId: string, toVizId: string, toTitle: string) {
  posthog.capture("related_chart_clicked", { from_viz_id: fromVizId, to_viz_id: toVizId, to_title: toTitle });
}

export function trackNavigation(destination: string) {
  posthog.capture("navigation_clicked", { destination });
}
