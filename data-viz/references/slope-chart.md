# Slope Chart

Compare values at two time points across many entities. Lines connect "before" to "after", colored by magnitude of change.

## Data Format

```javascript
const data = [
  {"n":"Japan","a":67.7,"b":84.0},
  {"n":"China","a":33.4,"b":78.0},
  // n = name, a = before value, b = after value
];
```

## Layout

- Two vertical axes (left = before, right = after)
- Lines connect each entity's before/after values
- Labels on both sides, collision-resolved
- Color encodes change magnitude

```
W = 700, H = 560
pad = { left: 120, right: 130, top: 40, bottom: 20 }
```

Left/right padding is wide (120-130px) to fit country name labels.

## Scaling

```javascript
const minV = 30, maxV = 86; // data-dependent range
const scale = v => pad.top + (maxV - v) / (maxV - minV) * (H - pad.top - pad.bottom);
```

## Color Encoding

Assign color by change magnitude (b - a):

```javascript
const colorForChange = d => {
  const change = d.b - d.a;
  if (change > 30) return "#EA5E33";  // accent
  if (change > 20) return "#F29A44";  // mid
  if (change > 15) return "#F5D38A";  // light
  return "#A6C4A2";                    // cool
};
```

Adapt thresholds to the data's distribution.

## Labels

Place labels at both endpoints. Run `resolveCollisions()` on each side independently with `minGap: 14`.

Left label format: `"CountryName  value"` (right-aligned)
Right label format: `"value  CountryName"` (left-aligned)

## Interactivity

Per-row hover. Each entity gets an invisible wide hit area (12px stroke, transparent) over the connecting line.

On hover:
- Dim all other rows to `opacity: 0.15`
- Show tooltip with: `"CountryName: before -> after (+change)"`

On mouseout: restore all rows to `opacity: 1`.

## Column Headers

Place year labels ("1960", "2023") at top of each axis using JetBrains Mono 10px, `#7A786F`.

## Legend

Optional. Place below chart or in top-right corner. Use colored swatches (small rects) with labels describing each threshold band.
