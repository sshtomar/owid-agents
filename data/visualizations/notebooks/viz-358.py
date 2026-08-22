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
        # Nuclear Electricity Share — Methodology

        Documents the data pipeline for viz-358: horizontal bar chart of
        nuclear electricity as % of total generation for the top nuclear nations.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_names = [
        "World", "income", "dividend", "Latin", "Arab", "Euro", "Africa",
        "Asia", "Pacific", "Europe", "Central", "North America", "OECD",
        "small states", "excluding", "fragile", "IDA", "IBRD",
        "Middle East", "Caribbean", "South Asia", "Upper middle",
        "Lower middle", "High income", "Low income"
    ]

    latest = {}
    for r in data:
        if r["value"] is not None and not any(x in r["countryName"] for x in agg_names):
            if r["countryName"] not in latest or r["year"] > latest[r["countryName"]]["year"]:
                latest[r["countryName"]] = r

    nuclear = sorted(
        [v for v in latest.values() if v["value"] > 0.5],
        key=lambda x: -x["value"]
    )[:20]

    print(f"Countries with nuclear electricity > 0.5%: {len(nuclear)}")
    for c in nuclear:
        label = c["countryName"].replace("Korea, Rep.", "South Korea")
        print(f"  {label} ({c['year']}): {c['value']:.1f}%")
    return latest, nuclear


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — ranked comparison of discrete values
        - **Country selection**: All countries with >0.5% nuclear share (most recent available year)
        - **Color**: Warm-to-cool by share; France at 67% is accent orange, bottom countries cool green
        - **Highlights**: France is an extreme outlier; Central/Eastern Europe clusters 40-42%; Germany at 1.4% shows post-phase-out residual
        """
    )
    return


@app.cell
def _(json, nuclear):
    label_map = {"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran"}
    chart_data = [
        {
            "n": label_map.get(c["countryName"], c["countryName"]),
            "v": round(c["value"], 1),
            "y": c["year"]
        }
        for c in nuclear
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
