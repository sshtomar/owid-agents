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
        # Population Growth Rate by World Region — Methodology

        Trend lines showing annual population growth rates (%) by world region from 1961 to 2024. Illustrates the global demographic transition with Sub-Saharan Africa as the clear outlier.
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
    regions = [
        "Sub-Saharan Africa", "South Asia", "East Asia & Pacific",
        "Europe & Central Asia", "Latin America & Caribbean",
        "North America"
    ]
    by_region = {}
    for row in data:
        c = row["countryName"]
        if c in regions and row["value"] is not None:
            by_region.setdefault(c, {})[row["year"]] = row["value"]

    print(f"Regions loaded: {list(by_region.keys())}")
    for r in regions:
        if r in by_region:
            yrs = sorted(by_region[r].keys())
            print(f"  {r}: {yrs[0]}-{yrs[-1]}, 2024={by_region[r].get(2024, 'n/a'):.2f}%")
    return by_region, regions


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — long time series shows demographic transition clearly
        - **Entity selection**: World Bank regional aggregates (not countries) for a clean macro story
        - **Time range**: 1961–2024 (64 years); Middle East excluded to keep 6 legible lines
        - **Highlights**: East Asia fell from 2.6% to 0.16%; Europe & C. Asia briefly went negative in 2022
        """
    )
    return


@app.cell
def _(json, by_region, regions):
    labels = {
        "East Asia & Pacific": "East Asia & Pacific",
        "Europe & Central Asia": "Europe & C. Asia",
        "Latin America & Caribbean": "Latin America",
        "Sub-Saharan Africa": "Sub-Saharan Africa",
        "North America": "North America",
        "South Asia": "South Asia",
    }
    chart_data = []
    for r in regions:
        if r in by_region:
            pts = [{"y": y, "v": round(by_region[r][y], 3)} for y in range(1961, 2025) if y in by_region[r]]
            chart_data.append({"n": labels.get(r, r), "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
