import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    return json, mo, Path


@app.cell
def _(mo):
    mo.md(
        """
        # Population Growth Rate, 1961–2024 — Methodology

        This notebook documents the data pipeline behind viz-358.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = {
        'Sub-Saharan Africa': 'Sub-Saharan Africa',
        'Ethiopia': 'Ethiopia',
        'India': 'India',
        'Brazil': 'Brazil',
        'Indonesia': 'Indonesia',
        'World': 'World',
        'Germany': 'Germany',
        'Japan': 'Japan',
        'Korea, Rep.': 'South Korea',
    }
    filtered = [d for d in data if d["value"] is not None and d["countryName"] in targets]
    print(f"Filtered to {len(filtered)} rows")
    return filtered, targets


@app.cell
def _(filtered, targets):
    from collections import defaultdict
    by_country = defaultdict(list)
    for p in filtered:
        label = targets[p["countryName"]]
        by_country[label].append((p["year"], round(p["value"], 2)))
    for name, pts in sorted(by_country.items()):
        pts.sort()
        print(f"{name}: {pts[0]} -> {pts[-1]}")
    return by_country,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows demographic convergence over six decades
        - **Country selection**: Covers the full spectrum from Sub-Saharan Africa (persistently high) to Japan (negative)
        - **Sampled every 5 years** to keep data size manageable
        - **Story**: Most of the world is converging toward low or negative growth; Africa is the exception
        """
    )
    return


@app.cell
def _(by_country, json):
    chart_data = [
        {"n": name, "pts": [{"y": y, "v": v} for y, v in sorted(pts) if y % 5 == 1 or y == 2024]}
        for name, pts in by_country.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
