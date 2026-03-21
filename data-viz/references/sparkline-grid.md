# Sparkline Grid

Compact grid of small trend charts. Each cell shows one entity's time series as a miniature line chart with start/end values.

## Data Format

```javascript
const data = [
  {"n":"Afghanistan","s":[353,327,312,290,270,250],"e":353,"l":56,"y0":1960},
  // n = name, s = series values, e = earliest value, l = latest value, y0 = start year
];
```

## Layout

CSS Grid with 6 columns (adapt to data count). Each cell is self-contained.

```css
.grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 0;
}
.cell {
  padding: 12px 10px;
  border-bottom: 1px solid #E2E0D5;
  border-right: 1px solid #E2E0D5;
  cursor: crosshair;
  position: relative;
}
```

## Rendering

Use Canvas for each cell (one canvas per cell, or one large canvas for the whole grid).

Per cell:
1. Country name (Inter 9px, 500 weight, `#2B2A27`) at top-left
2. Sparkline filling the cell width, normalized to each entity's own min/max
3. Start value (left-aligned, JetBrains Mono 8px, `#7A786F`) and end value (right-aligned)

```javascript
// Normalize series to cell height
const min = Math.min(...series);
const max = Math.max(...series);
const norm = v => cellH - ((v - min) / (max - min)) * cellH;
```

## Line Style

```javascript
ctx.strokeStyle = "#EA5E33";
ctx.lineWidth = 1.2;
ctx.lineJoin = "round";
ctx.beginPath();
series.forEach((v, i) => {
  const x = (i / (series.length - 1)) * cellW;
  const y = norm(v);
  i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
});
ctx.stroke();
```

## Interactivity

On mousemove over a cell:
- Calculate which data point is nearest using x-position ratio
- Draw a vertical crosshair line at that x position
- Show tooltip with year and value

```javascript
const ratio = mx / cellWidth;
const idx = Math.round(ratio * (series.length - 1));
const year = startYear + idx;
const value = series[idx];
```

## Sorting

Sort entities by a meaningful metric (highest initial value, largest absolute drop, etc.) before rendering. The sort order is part of the story.
