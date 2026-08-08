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
        # Arable Land per Person, 1961–2023 — Methodology

        This notebook documents the data pipeline behind viz-359.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-LND-ARBL-HA-PC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = {
        'World': 'World',
        'Sub-Saharan Africa': 'Sub-Saharan Africa',
        'India': 'India',
        'Canada': 'Canada',
        'China': 'China',
        'Bangladesh': 'Bangladesh',
        'Egypt, Arab Rep.': 'Egypt',
    }
    filtered = [d for d in data if d["value"] is not None and d["countryName"] in targets]
    print(f"Filtered to {len(filtered)} rows")
    return filtered, targets


@app.cell
def _(filtered, targets):
    from collections import defaultdict
    by_entity = defaultdict(list)
    for p in filtered:
        label = targets[p["countryName"]]
        by_entity[label].append((p["year"], round(p["value"], 3)))
    for name, pts in sorted(by_entity.items()):
        pts.sort()
        print(f"{name}: {pts[0]} -> {pts[-1]}")
    return by_entity,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the long-run decline in arable land per capita
        - **Entities**: World average + range from Canada (spacious) to Egypt (land-scarce)
        - **Story**: Global arable land per person has halved since 1961; densely populated countries face acute food security pressure from land squeeze
        - **Sampled every 5 years** for readability
        """
    )
    return


@app.cell
def _(by_entity, json):
    chart_data = [
        {"n": name, "pts": [{"y": y, "v": v} for y, v in sorted(pts) if y % 5 == 1 or y == 2023]}
        for name, pts in by_entity.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
