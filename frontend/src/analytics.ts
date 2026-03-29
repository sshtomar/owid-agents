/// <reference types="vite/client" />
import posthog from "posthog-js";

// Initialize PostHog - replace with your project API key and host
const POSTHOG_KEY = (import.meta as any).env?.VITE_POSTHOG_KEY || "";
const POSTHOG_HOST =
  (import.meta as any).env?.VITE_POSTHOG_HOST || "https://us.i.posthog.com";

let initialized = false;

export function initPostHog() {
  if (initialized || !POSTHOG_KEY) return;
  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    capture_pageview: false, // we handle this manually with the router
    capture_pageleave: true,
    autocapture: true,
  });
  initialized = true;
}

export function capturePageView(path: string) {
  if (!POSTHOG_KEY) return;
  posthog.capture("$pageview", { $current_url: window.location.origin + path });
}

export function captureGraphView(vizId: string, title: string, chartType: string) {
  if (!POSTHOG_KEY) return;
  posthog.capture("graph_viewed", {
    viz_id: vizId,
    viz_title: title,
    chart_type: chartType,
  });
}

export function captureDatasetView(datasetId: string) {
  if (!POSTHOG_KEY) return;
  posthog.capture("dataset_viewed", { dataset_id: datasetId });
}

export function captureGalleryCardClick(vizId: string, title: string) {
  if (!POSTHOG_KEY) return;
  posthog.capture("gallery_card_clicked", {
    viz_id: vizId,
    viz_title: title,
  });
}
