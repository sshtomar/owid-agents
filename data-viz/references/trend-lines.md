# Trend Lines

Multiple overlapping time series lines with hover isolation. For showing how many entities evolved over time (e.g. fertility rates 1960-2023 for 10 countries).

## Data Format

```javascript
const data = [
  {"n":"South Korea","s":[4.5,4.2,3.8,2.9,1.6,1.2,1.1,0.72],"y0":1970,"step":5},
  {"n":"Iran","s":[7.5,6.8,5.0,2.8,2.0,1.8,1.7],"y0":1970,"step":5},
  // n = name, s = values, y0 = start year, step = years between values
];
```

If step varies, use explicit year-value pairs:

```javascript
const data = [
  {"n":"Brazil","pts":[{"y":1960,"v":6.1},{"y":1970,"v":5.0},...]},
];
```

## Layout

```javascript
const W = 800, H = 460;
const margin = { top: 30, right: 120, bottom: 30, left: 50 };
// Right margin wide for endpoint labels
```

## Scales

```javascript
const xScale = year => margin.left +
  (year - yearMin) / (yearMax - yearMin) * (W - margin.left - margin.right);

const yScale = val => margin.top +
  (valMax - val) / (valMax - valMin) * (H - margin.top - margin.bottom);
```

## Rendering

Use SVG. Each entity gets a `<g>` group containing:
1. A `<path>` for the line
2. An endpoint label (right side)
3. An invisible wide `<path>` (stroke-width 12, transparent) for hover hit detection

```javascript
const pathD = points.map((p, i) =>
  `${i === 0 ? "M" : "L"} ${xScale(p.year)} ${yScale(p.value)}`
).join(" ");

const line = mkEl("path", {
  d: pathD,
  stroke: lineColor,
  "stroke-width": "1.5",
  fill: "none",
  "stroke-linejoin": "round",
});
```

## Color Assignment

For <8 entities, assign distinct colors from the palette. For 8+ entities, color by a categorical attribute (e.g. region, improvement band).

Improvement-band coloring:

```javascript
function colorForChange(pctDecline) {
  if (pctDecline > 70) return "#3D7A5A";
  if (pctDecline > 50) return "#5B9E78";
  if (pctDecline > 40) return "#8BAD72";
  if (pctDecline > 30) return "#C49A45";
  if (pctDecline > 20) return "#C4715A";
  return "#B34B3B";
}
```

## Endpoint Labels

Place at the right edge, aligned to the final data point's y-position. Run `resolveCollisions()` with `minGap: 12` to prevent overlap.

Format: `"value  CountryName"` in JetBrains Mono 9px.

## Interactivity

On hover over an invisible hit path:
- Set all other lines to `opacity: 0.1`
- Thicken hovered line to `stroke-width: 3`
- Show tooltip tracking mouse with nearest year's value

Nearest-year detection along the hovered line:

```javascript
const rect = svg.getBoundingClientRect();
const mx = e.clientX - rect.left;
const ratio = (mx - margin.left) / (W - margin.left - margin.right);
const yearIdx = Math.round(ratio * (series.length - 1));
const year = startYear + yearIdx * step;
```

## Reference Lines

Add horizontal dashed lines for meaningful thresholds:

```javascript
// e.g. replacement fertility rate
svg.appendChild(mkEl("line", {
  x1: margin.left, y1: yScale(2.1),
  x2: W - margin.right, y2: yScale(2.1),
  stroke: "#C2C0B5", "stroke-dasharray": "4,3", "stroke-width": "0.5"
}));
```

Label the reference line at its right endpoint.

## Annotation Bands

Optionally highlight a dangerous or notable value range with a semi-transparent background rect:

```javascript
svg.appendChild(mkEl("rect", {
  x: margin.left, y: yScale(bandMax),
  width: W - margin.left - margin.right,
  height: yScale(bandMin) - yScale(bandMax),
  fill: "#EA5E33", opacity: "0.06"
}));
```
