# Dot Matrix

Compare many entities across many metrics in a single compact grid. Each cell contains a dot sized and colored by normalized value.

## Data Format

```javascript
const data = [
  {"c":"JP","life_exp":84.0,"gdp_pc":32487,"mortality":2.4,"urban":92.2,"internet":87.0,"renewable":21.1},
  {"c":"AU","life_exp":83.1,"gdp_pc":55120,"mortality":3.7,"urban":86.6,"internet":96.0,"renewable":24.8},
];

const metrics = [
  {key: "life_exp", label: "Life Exp.", unit: "yrs", invert: false},
  {key: "mortality", label: "Under-5 Mort.", unit: "/1k", invert: true},
  // invert: true means lower values are better (green)
];
```

## Layout

Use Canvas. Rows = entities (countries), columns = metrics.

```javascript
const rowH = 28;
const colW = 90;
const labelW = 100;  // left column for country names
const headerH = 50;  // top row for metric labels
```

## Normalization

Per-column normalization to [0, 1]:

```javascript
metrics.forEach(m => {
  const vals = data.map(d => d[m.key]);
  m.min = Math.min(...vals);
  m.max = Math.max(...vals);
});

function normalize(value, metric) {
  let n = (value - metric.min) / (metric.max - metric.min);
  if (metric.invert) n = 1 - n;
  return n;
}
```

## Dot Rendering

Each dot: circle centered in its cell, radius scaled by normalized value, color interpolated from a gradient.

```javascript
const r = 3 + normalize(value, metric) * 8;  // radius range: 3-11

function dotColor(n) {
  // Interpolate: low (cool grey) -> mid (amber) -> high (green)
  if (n > 0.7) return interpolate(mid, high, (n - 0.7) / 0.3);
  if (n > 0.3) return interpolate(low, mid, (n - 0.3) / 0.4);
  return interpolate(vlow, low, n / 0.3);
}
```

## Color Interpolation

```javascript
function interpolate(c1, c2, t) {
  return [
    Math.round(c1[0] + (c2[0] - c1[0]) * t),
    Math.round(c1[1] + (c2[1] - c1[1]) * t),
    Math.round(c1[2] + (c2[2] - c1[2]) * t),
  ];
}

const low  = [194, 192, 181];  // #C2C0B5 (grey)
const mid  = [234, 94, 51];    // #EA5E33 (accent)
const high = [61, 122, 90];    // #3D7A5A (green)
```

## Headers

Draw metric labels rotated or horizontal at the top of each column. Use JetBrains Mono 8px, `#7A786F`.

## Row Labels

Country names in the left column. Inter 10px, 500 weight. Highlight current row on hover.

## Interactivity

Track mouse position, calculate which row and column the cursor is in:

```javascript
canvas.addEventListener("mousemove", e => {
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;
  const row = Math.floor((my - headerH) / rowH);
  const col = Math.floor((mx - labelW) / colW);
  draw(row, col);  // redraw with highlight state
});
```

On hover:
- Highlight the entire row (bolder text, slight background tint)
- Highlight the column header
- Show tooltip with: `"Country: metric = value (unit)"`

On mouseout: `draw(-1, -1)` to clear highlights.

## Sorting

Sort rows by a default metric (e.g. life expectancy descending). Consider letting the most "interesting" metric drive the sort.
