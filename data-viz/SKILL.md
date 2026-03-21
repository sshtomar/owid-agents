---
name: data-viz
description: >
  Create self-contained, interactive data visualizations as single HTML files using vanilla SVG or Canvas.
  Designed for public dataset storytelling (World Bank, WHO, UN) with inline data, hover tooltips, and
  a warm editorial design system. Use when asked to: (1) visualize a dataset, (2) create a chart or
  graph from data, (3) build an interactive data story, (4) compare countries or indicators over time,
  (5) generate an embeddable standalone HTML visualization. Triggers on: "make a chart", "visualize this
  data", "create a visualization", "build an interactive chart", "plot this data", "data story".
---

# Data Viz

Single-file, self-contained HTML visualizations with inline data, hover interactivity, and an editorial design system. No build tools, no dependencies, no external data files.

## Design System

See [references/design-system.md](references/design-system.md) for the full color palette, typography scale, and CSS boilerplate.

## Chart Types

Each chart type has a reference with data format, rendering approach, and interactivity pattern.

| Type | When to use | Reference |
|---|---|---|
| **Slope chart** | Compare values at two time points across many entities | [references/slope-chart.md](references/slope-chart.md) |
| **Sparkline grid** | Show many small trend lines in a compact grid | [references/sparkline-grid.md](references/sparkline-grid.md) |
| **Trail chart** | Trace entities through 2D space over time (e.g. GDP vs life expectancy) | [references/trail-chart.md](references/trail-chart.md) |
| **Dot matrix** | Compare many entities across many metrics in a single view | [references/dot-matrix.md](references/dot-matrix.md) |
| **Trend lines** | Show time series for multiple entities with hover isolation | [references/trend-lines.md](references/trend-lines.md) |

For chart types not listed, follow the core patterns from the design system and adapt the rendering approach.

## Workflow

1. **Pick the story.** Decide what comparison or trend to highlight before touching code. Write the title and 2-3 highlights first.
2. **Shape the data.** Subset to 10-25 entities. Remove nulls. Inline as a JS array at the top of the script block.
3. **Pick a chart type.** Read the matching reference file for the data format and rendering pattern.
4. **Render.** Use raw SVG DOM (`createElementNS`) for <50 elements, Canvas for dense grids.
5. **Add interactivity.** Every chart needs a tooltip and a highlight-on-hover state.
6. **Attribute the source.** Footer line with dataset name and provider.

## Constraints

- Single HTML file, no external data files or JS imports (fonts from Google Fonts CDN are OK).
- Keep under 500KB. Trim data to key entities and years.
- Vanilla JS only: SVG DOM manipulation or Canvas 2D. No charting libraries.
- Must render at `file://` protocol (opened directly in a browser).
- Responsive via SVG `viewBox` with `width="100%"` and a `maxWidth` cap.

## Data Embedding

Inline data as a JS const at the top of the `<script>` block. Use short property names to save bytes.

```javascript
// Slope chart: {n: name, a: before, b: after}
const data = [{"n":"Japan","a":67.7,"b":84.0}, ...];

// Time series: {n: name, s: [values], y0: startYear}
const data = [{"n":"Afghanistan","s":[353,327,312],"y0":1960}, ...];

// Scatter/trail: {c: country, y: year, x: xVal, v: yVal}
const raw = [{"c":"US","y":1960,"x":3007,"v":69.8}, ...];

// Matrix: {c: code, ...metrics}
const data = [{"c":"JP","life":84.0,"gdp":32487,"mort":2.4}, ...];
```

## Interactivity

Every chart uses a tooltip div and highlight-on-hover:

```javascript
const tip = document.getElementById("tip");
function showTip(text, e) {
  tip.textContent = text;
  tip.style.opacity = "1";
  tip.style.left = (e.clientX + 12) + "px";
  tip.style.top = (e.clientY - 20) + "px";
}
function hideTip() { tip.style.opacity = "0"; }
```

Highlight: dim all elements to `opacity: 0.15`, keep hovered element at full opacity with thicker stroke.

## Label Collision Resolution

When labels overlap (slope charts, trend endpoints), spread them iteratively:

```javascript
function resolveCollisions(items, minGap) {
  const sorted = items.slice().sort((a, b) => a.y - b.y);
  for (let pass = 0; pass < 20; pass++) {
    let moved = false;
    for (let i = 1; i < sorted.length; i++) {
      const gap = sorted[i].y - sorted[i - 1].y;
      if (gap < minGap) {
        const shift = (minGap - gap) / 2;
        sorted[i - 1].y -= shift;
        sorted[i].y += shift;
        moved = true;
      }
    }
    if (!moved) break;
  }
  return sorted;
}
```
