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
        # Greenhouse Gas Emissions: Key Economies -- Methodology

        Trend lines of total GHG emissions (excluding land-use change)
        for 12 major economies, 1990-2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-GHG-ALL-MT-CE-AR5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {
        "China": "China", "India": "India", "Brazil": "Brazil",
        "Indonesia": "Indonesia", "Japan": "Japan", "Iran, Islamic Rep.": "Iran",
        "Germany": "Germany", "Korea, Rep.": "South Korea",
        "Canada": "Canada", "Australia": "Australia",
        "France": "France", "Argentina": "Argentina",
    }
    years = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2022]
    result = []
    for orig, label in target.items():
        pts_map = {p["year"]: p["value"] for p in data if p["countryName"] == orig and p["value"] is not None}
        pts = [{"y": y, "v": round(pts_map[y], 0)} for y in years if y in pts_map]
        if len(pts) >= 7:
            result.append({"n": label, "pts": pts})
    print(f"Series: {len(result)}")
    for s in sorted(result, key=lambda x: -x['pts'][-1]['v']):
        print(f"  {s['n']}: {s['pts'][0]['v']:.0f} -> {s['pts'][-1]['v']:.0f} Mt")
    return result, target, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectories over time for multiple entities
        - **Country selection**: Major economies with available data; note US and Russia absent from this WB series
        - **Time range**: 1990-2022 to capture post-Cold-War emissions growth
        - **Color**: Warm (orange/red) for high 2022 emitters, cool (green) for low emitters
        - **Highlights**: China quadrupled emissions since 1990; Japan and Germany declining
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
