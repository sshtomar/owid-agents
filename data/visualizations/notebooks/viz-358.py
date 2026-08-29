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
        # Wind Electricity Generation -- Methodology

        Documents the data pipeline behind viz-358.
        Source: ember--GEN-WIND (Ember Climate, 2010 vs 2024 comparison)
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-WIND.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    top_countries = [
        "China", "United States of America", "Germany", "Brazil",
        "United Kingdom", "India", "Spain", "Canada", "France",
        "Sweden", "Turkey", "Netherlands"
    ]
    pts = {}
    for p in data:
        if p["countryName"] in top_countries and p["value"] is not None:
            if p["countryName"] not in pts:
                pts[p["countryName"]] = {}
            pts[p["countryName"]][p["year"]] = p["value"]

    slope = []
    for c in top_countries:
        if c in pts and 2010 in pts[c] and 2024 in pts[c]:
            slope.append({
                "n": c,
                "a": round(pts[c][2010], 1),
                "b": round(pts[c][2024], 1)
            })
    print(json.dumps(slope, separators=(",", ":")))
    return pts, slope, top_countries


if __name__ == "__main__":
    app.run()
