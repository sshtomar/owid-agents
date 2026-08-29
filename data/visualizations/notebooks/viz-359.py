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
        # Nuclear Electricity Generation -- Methodology

        Documents the data pipeline behind viz-359.
        Source: ember--GEN-NUCLEAR (Ember Climate, 2000-2024)

        Key stories:
        - USA: stable dominance ~780-810 TWh
        - China: rapid rise from 17 to 451 TWh
        - France: high but declining (Fukushima policy aftermath + aging reactors)
        - Japan: dramatic collapse in 2011-2012 (Fukushima), slow recovery
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-NUCLEAR.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    top_countries = [
        "United States of America", "China", "France",
        "Russian Federation (the)", "South Korea", "Canada",
        "Japan", "India", "Sweden"
    ]
    pts = {}
    for p in data:
        if p["countryName"] in top_countries and p["value"] is not None and p["value"] > 0:
            if p["countryName"] not in pts:
                pts[p["countryName"]] = {}
            pts[p["countryName"]][p["year"]] = p["value"]

    series = []
    for c in top_countries:
        years_vals = sorted(pts.get(c, {}).items())
        years_vals_filtered = [(y, v) for y, v in years_vals if 2000 <= y <= 2024]
        series.append({"n": c, "pts": [{"y": y, "v": round(v, 1)} for y, v in years_vals_filtered]})
    print(json.dumps(series, separators=(",", ":")))
    return pts, series, top_countries


if __name__ == "__main__":
    app.run()
