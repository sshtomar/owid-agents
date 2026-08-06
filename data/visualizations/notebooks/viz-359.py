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
        # Population Growth Rate — Methodology

        Visualizes annual population growth rates from 1961 to 2024 for 7 countries,
        illustrating the global demographic transition from high to low (or negative) growth.
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
    from collections import defaultdict
    by_country = defaultdict(list)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]].append((pt["year"], pt["value"]))
    return by_country, defaultdict


@app.cell
def _(by_country, json):
    selected = ["Ethiopia","India","Indonesia","Brazil","China","Germany","Japan"]
    chart_data = []
    for c in selected:
        if c not in by_country:
            print(f"Missing: {c}")
            continue
        all_pts = {y: v for y, v in by_country[c]}
        series = [round(all_pts.get(yr), 2) if all_pts.get(yr) is not None else None for yr in range(1961, 2025)]
        chart_data.append({"n": c, "s": series, "y0": 1961})
    print(f"Chart data ({len(chart_data)} countries):")
    for row in chart_data:
        vals = [v for v in row["s"] if v is not None]
        print(f"  {row['n']}: {vals[0]}% (1961) -> {vals[-1]}% (latest)")
    print(json.dumps(chart_data, separators=(",", ":")))
    return c, chart_data, selected


if __name__ == "__main__":
    app.run()
