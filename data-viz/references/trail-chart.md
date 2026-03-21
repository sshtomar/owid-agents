# Trail Chart

Trace entities through 2D space over time. Each entity draws a path through (x, y) coordinates across decades (e.g. GDP vs life expectancy from 1960 to 2023).

## Data Format

```javascript
const raw = [
  {"c":"United States","y":1960,"le":69.8,"gdp":3007},
  {"c":"United States","y":1965,"le":70.2,"gdp":3828},
  // One row per country per time step (typically every 5 years)
];
```

Group by country at render time:

```javascript
const countries = [...new Set(raw.map(d => d.c))];
const byCountry = {};
countries.forEach(c => { byCountry[c] = raw.filter(d => d.c === c); });
```

## Scales

X-axis is often logarithmic (GDP spans orders of magnitude):

```javascript
const xMin = 70, xMax = 100000;
const xScale = v => margin.left +
  (Math.log10(v) - Math.log10(xMin)) /
  (Math.log10(xMax) - Math.log10(xMin)) * innerW;
```

Y-axis is linear:

```javascript
const yMin = 30, yMax = 90;
const yScale = v => margin.top +
  (yMax - v) / (yMax - yMin) * innerH;
```

## Rendering

For each country, draw a path connecting its data points in time order. Use SVG `<path>` elements.

```javascript
const pathD = points.map((p, i) =>
  `${i === 0 ? "M" : "L"} ${xScale(p.gdp)} ${yScale(p.le)}`
).join(" ");
```

Add dots at each time step. Label the first and last year at the path endpoints.

## Path Style

```javascript
path.setAttribute("stroke", countryColor);
path.setAttribute("stroke-width", "1.5");
path.setAttribute("fill", "none");
path.setAttribute("stroke-linejoin", "round");
```

Dots: filled circles, r=2.5 for intermediate points, r=4 for endpoints.

## Color Assignment

Assign each country a distinct color. With 6 countries, use:

```javascript
const palette = ["#EA5E33", "#2B8A6F", "#5B7CC2", "#C4715A", "#8B6DAE", "#3D7A5A"];
```

## Interactivity

On hover, highlight one country's trail:
- Set all other paths to `opacity: 0.1`
- Thicken the hovered path to `stroke-width: 3`
- Show tooltip with country name, year, x-value, y-value for the nearest point

Nearest-point detection:

```javascript
let best = null, bestDist = Infinity;
allDots.forEach(dot => {
  const dx = dot.sx - mx, dy = dot.sy - my;
  const dist = dx * dx + dy * dy;
  if (dist < bestDist) { bestDist = dist; best = dot; }
});
```

## Axis Labels

- X-axis: logarithmic ticks at powers of 10 (100, 1K, 10K, 100K). Format with `$` prefix for money.
- Y-axis: linear ticks at round intervals (40, 50, 60, 70, 80). Label units (e.g. "years").

## Annotations

Optionally label notable moments on a trail (e.g. "1995: Japan's GDP stagnates") using small text anchored to the nearest dot.
