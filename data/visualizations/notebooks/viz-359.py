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
        # Age Dependency Ratio by Country, 1960–2024 -- Methodology

        This notebook documents the data pipeline behind viz-359, a trend lines chart
        showing diverging demographic trajectories: sub-Saharan Africa maintains very
        high dependency ratios (many dependents per worker) while East Asia has seen
        dramatic falls followed by a new rise as populations age.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    COUNTRIES = [
        "Niger", "Chad", "Angola",
        "Japan", "Italy", "Germany",
        "China", "Brazil", "Iran, Islamic Rep.", "Thailand",
        "France", "United States",
    ]
    by_country = {}
    for row in data:
        if row["countryName"] in COUNTRIES and row["value"] is not None:
            by_country.setdefault(row["countryName"], {})[row["year"]] = row["value"]

    for c in COUNTRIES:
        if c in by_country:
            vs = by_country[c]
            print(f"  {c}: 1960={vs.get(1960,'-'):.0f}%, 2024={vs.get(2024,vs.get(2023,'-')):.0f}%")
    return COUNTRIES, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- multi-series from 1960 to 2024
        - **Groups**: Sub-Saharan Africa (high, young), East Asia + rapid-transition (falling then rising), Europe/NA (aging)
        - **Color**: by group — red family for high-dependency Africa, cool greens for rapid transitions, muted for Europe
        - **Highlights**:
          - Niger/Chad: dependency ratio above 100% (more dependents than workers) throughout
          - China: fell from 80% to 37% as one-child policy took effect, now rising again
          - Japan/Germany: U-shaped curve (was high in 1960, fell, now aging past 65%)
          - Iran: sharp fall from 95% to 40% in one generation, then leveling
        """
    )
    return


@app.cell
def _(json, COUNTRIES, by_country):
    LABELS = {"Iran, Islamic Rep.": "Iran"}
    chart_data = []
    for c in COUNTRIES:
        if c not in by_country:
            continue
        vs = by_country[c]
        series = [round(vs[y], 1) if y in vs else None for y in range(1960, 2025)]
        label = LABELS.get(c, c)
        chart_data.append({"n": label, "s": series, "y0": 1960})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
