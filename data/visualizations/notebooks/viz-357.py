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
        # Solar Electricity Generation -- Methodology

        Documents the data pipeline behind viz-357.
        Source: ember--GEN-SOLAR (Ember Climate, 2000-2024)
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-SOLAR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    top_countries = [
        "China", "United States of America", "India", "Japan", "Germany",
        "Brazil", "Spain", "Australia", "Italy", "South Korea"
    ]
    pts = {}
    for p in data:
        if p["countryName"] in top_countries and p["value"] is not None:
            if p["countryName"] not in pts:
                pts[p["countryName"]] = {}
            pts[p["countryName"]][p["year"]] = p["value"]
    return pts, top_countries


@app.cell
def _(json, pts, top_countries):
    series = []
    for c in top_countries:
        years_vals = sorted(pts.get(c, {}).items())
        filtered = [(y, v) for y, v in years_vals if v is not None and v > 0]
        series.append({"n": c, "pts": [{"y": y, "v": round(v, 1)} for y, v in filtered]})
    print(json.dumps(series, separators=(",", ":")))
    return (series,)


if __name__ == "__main__":
    app.run()
