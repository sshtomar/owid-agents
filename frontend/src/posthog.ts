import posthog from "posthog-js";

let initialized = false;

export function initPostHog() {
  if (initialized) return;
  initialized = true;
  posthog.init("phc_x0nmATrfOEVbCKfBaYBqs0ATawOCEICzWc00H35p49g", {
    api_host: "https://us.i.posthog.com",
    person_profiles: "identified_only",
    capture_pageview: false, // we handle this manually with react-router
    capture_pageleave: true,
  });
}

export default posthog;
