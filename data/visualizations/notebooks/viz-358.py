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
        # International Tourism Arrivals — Methodology

        Visualizes tourist arrivals for top 10 destinations from 1995 to 2020,
        highlighting the dramatic COVID-19 collapse in 2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]].append((pt["year"], pt["value"]))
    return by_country, defaultdict


@app.cell
def _(by_country, json):
    selected = ["France","China","Italy","Germany","Greece","Austria","Japan","Korea, Rep.","Croatia","Denmark"]
    chart_data = []
    for c in selected:
        if c not in by_country:
            print(f"Missing: {c}")
            continue
        all_pts = {y: v for y, v in by_country[c]}
        series = [round(all_pts.get(yr) / 1e6, 1) if all_pts.get(yr) is not None else None for yr in range(1995, 2021)]
        chart_data.append({"n": c, "s": series, "y0": 1995})
    print(f"Chart data ({len(chart_data)} countries):")
    for row in chart_data:
        vals = [v for v in row["s"] if v is not None]
        print(f"  {row['n']}: peak={max(vals):.1f}M, 2020={vals[-1]:.1f}M")
    print(json.dumps(chart_data, separators=(",", ":")))
    return c, chart_data, selected


if __name__ == "__main__":
    app.run()
