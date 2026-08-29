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
        # Arable Land -- Methodology

        Documents the data pipeline behind viz-360.
        Source: wb--AG-LND-ARBL-ZS (World Bank, 2000 vs 2022)

        Story: South/East Asian densely farmed nations slowly losing arable land
        to urbanization; West Africa & South America expanding cultivation.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-LND-ARBL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    selected = [
        "Bangladesh", "Denmark", "India", "Hungary", "Germany",
        "France", "Italy", "Czechia", "Argentina", "China",
        "Kenya", "Indonesia", "Brazil", "Egypt, Arab Rep.", "Burundi"
    ]
    pts = {}
    for p in data:
        if p["countryName"] in selected and p["value"] is not None:
            if p["countryName"] not in pts:
                pts[p["countryName"]] = {}
            pts[p["countryName"]][p["year"]] = p["value"]

    slope = []
    for c in selected:
        if c in pts and 2000 in pts[c] and 2022 in pts[c]:
            slope.append({
                "n": c,
                "a": round(pts[c][2000], 1),
                "b": round(pts[c][2022], 1)
            })
    slope.sort(key=lambda x: x["b"], reverse=True)
    print(json.dumps(slope, separators=(",", ":")))
    return pts, slope, selected


if __name__ == "__main__":
    app.run()
