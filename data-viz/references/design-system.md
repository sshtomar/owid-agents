# Design System

## Color Palette

| Token | Hex | Usage |
|---|---|---|
| `bg` | `#F6F5EE` | Page and chart background |
| `text-primary` | `#2B2A27` | Titles, primary labels |
| `text-secondary` | `#7A786F` | Subtitles, axis labels, source |
| `text-tertiary` | `#9A9890` | De-emphasized metadata |
| `accent` | `#EA5E33` | Primary highlight, largest change |
| `accent-mid` | `#F29A44` | Medium-range values |
| `accent-light` | `#F5D38A` | Low-range values |
| `cool` | `#A6C4A2` | Minimal change, contrast to warm tones |
| `border` | `#E2E0D5` | Grid lines, chart frames |
| `border-strong` | `#C2C0B5` | Section dividers |
| `tooltip-bg` | `#2B2A27` | Tooltip background |
| `tooltip-text` | `#F6F5EE` | Tooltip text |

### Sequential warm ramp (for ranked data)

```
#EA5E33 -> #F29A44 -> #F5D38A -> #A6C4A2
(highest)                        (lowest)
```

### Diverging ramp (for improvement categories)

```
#3D7A5A  70%+ improvement (deep green)
#5B9E78  50-70%
#8BAD72  40-50%
#C49A45  30-40% (amber)
#C4715A  20-30% (terra)
#B34B3B  <20%   (deep terra)
```

## Typography

**Fonts:** Import from Google Fonts CDN.

```css
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');
```

| Element | Font | Size | Weight | Extras |
|---|---|---|---|---|
| Chart title (h1) | Inter | 15px | 600 | letter-spacing: -0.3px |
| Subtitle (.subtitle) | Inter | 11px | 400 | color: #7A786F, max-width: 520px, line-height: 1.5 |
| Source (.source) | JetBrains Mono | 9px | 400 | uppercase, letter-spacing: 0.3px |
| Axis labels | JetBrains Mono | 9-10px | 400 | color: #7A786F |
| Data labels | Inter | 9-10px | 500 | color: #2B2A27 |
| Tooltip | JetBrains Mono | 10px | 400 | - |

## HTML Boilerplate

Every visualization uses this shell:

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');
  body { font-family: 'Inter', sans-serif; margin: 0; padding: 32px 40px; background: #F6F5EE; color: #2B2A27; }
  h1 { font-size: 15px; font-weight: 600; letter-spacing: -0.3px; margin: 0 0 4px; color: #2B2A27; }
  .subtitle { font-size: 11px; color: #7A786F; margin: 0 0 24px; max-width: 520px; line-height: 1.5; }
  .source { font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #7A786F; margin-top: 20px; letter-spacing: 0.3px; text-transform: uppercase; }
  svg text { font-family: 'Inter', sans-serif; }
  .tooltip { position: absolute; pointer-events: none; background: #2B2A27; color: #F6F5EE; font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 6px 10px; border-radius: 2px; white-space: nowrap; opacity: 0; transition: opacity 0.15s; z-index: 10; }
</style></head><body>
<h1>TITLE</h1>
<p class="subtitle">DESCRIPTION</p>
<div id="chart" style="position:relative;"></div>
<div class="tooltip" id="tip"></div>
<p class="source">Source: ATTRIBUTION</p>
<script>
const data = [/* inline data */];

// rendering code here

</script>
</body></html>
```

## SVG Setup

For SVG-based charts, create the root element with a fixed viewBox and fluid width:

```javascript
const W = 700, H = 460;
const margin = { top: 40, right: 120, bottom: 30, left: 60 };

const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
svg.setAttribute("width", "100%");
svg.style.maxWidth = W + "px";
svg.style.cursor = "crosshair";
document.getElementById("chart").appendChild(svg);
```

Helper for creating SVG elements:

```javascript
function mkEl(tag, attrs) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}
```

## Canvas Setup

For dense charts (grids, matrices), use Canvas with device pixel ratio:

```javascript
const canvas = document.getElementById("canvas");
const dpr = window.devicePixelRatio || 1;
const W = 800, H = 500;
canvas.width = W * dpr;
canvas.height = H * dpr;
canvas.style.width = W + "px";
canvas.style.height = H + "px";
const ctx = canvas.getContext("2d");
ctx.scale(dpr, dpr);
```

## Grid Lines

Subtle horizontal grid lines at major tick values:

```javascript
[40, 50, 60, 70, 80].forEach(v => {
  svg.appendChild(mkEl("line", {
    x1: margin.left, y1: yScale(v),
    x2: W - margin.right, y2: yScale(v),
    stroke: "#E2E0D5", "stroke-width": "0.5"
  }));
});
```

## Tooltip CSS

Already included in the boilerplate. Position with `position: absolute` (relative to chart container) or `position: fixed` (relative to viewport). Use `fixed` when the chart container is inside a scrollable parent.
