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
        # Poverty at National Lines — Methodology

        Trend lines showing how poverty rates (at each country's own national
        poverty line) have evolved since the 1990s for 8 countries with
        long, consistent time series and notable trajectories.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-POV-NAHC.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {raw['meta']['title']}")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict
    exclude_kw = [
        "IDA", "IBRD", "Sub-Saharan", "Least", "Heavily", "Low income",
        "Lower middle", "Africa Eastern", "Africa Western", "dividend",
        "Fragile", "World", "Upper middle", "East Asia", "South Asia",
        "Latin America", "Middle East", "Europe", "Central Asia",
        "Arab World", "Caribbean", "Pacific", "North America", "OECD",
        "Euro area", "demographic", "developing", "small states", "High income",
        "Post-demographic", "Central Europe", "European Union", "Middle income",
    ]
    by_country = defaultdict(list)
    for r in data:
        name = r["countryName"]
        if any(kw.lower() in name.lower() for kw in exclude_kw):
            continue
        if r["value"] is None:
            continue
        by_country[name].append((r["year"], r["value"]))
    print(f"Countries: {len(by_country)}")
    return (by_country,)


@app.cell
def _(by_country):
    selected = ["Costa Rica", "Chile", "Belarus", "Armenia", "Georgia", "Ecuador", "Indonesia", "Colombia"]
    chart_data = []
    for c in selected:
        series = sorted(by_country.get(c, []))
        if series:
            pts = [{"y": yr, "v": round(v, 1)} for yr, v in series]
            chart_data.append({"n": c, "pts": pts})
            print(f"{c}: {series[0]} -> {series[-1]} ({len(series)} pts)")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectories over time, not just snapshots
        - **Country selection**: Mix of Latin America (Chile 45%→7%, Ecuador), Eastern Europe
          (Belarus 39%→4%, Georgia, Armenia), Southeast Asia (Indonesia), Central America (Costa Rica)
        - **Story**: Chile's sustained 30-year decline is striking; COVID-19 caused visible upticks
          in 2020 across most countries
        - **Caveat**: National poverty lines differ across countries; this shows within-country
          progress, not cross-country comparisons
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
