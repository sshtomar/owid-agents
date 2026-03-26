import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # CO2 Emissions from Fuel Combustion -- Methodology

        This notebook documents the data pipeline and editorial decisions
        behind the visualization of CO2 emissions for the world's largest emitters.
        """
    )
    return


@app.cell
def _():
    import json
    return (json,)


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--9-4-1--EN_ATM_CO2.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = [
        "China", "United States of America", "India", "Russian Federation",
        "Japan", "Germany", "Republic of Korea", "Canada", "Indonesia",
        "Brazil", "Iran (Islamic Republic of)"
    ]
    filtered = [d for d in data if d["countryName"] in targets and d["value"] is not None]
    print(f"After filtering to target countries and removing nulls: {len(filtered)} rows")
    return filtered, targets


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.2f} - {max(values):.2f}")
    print(f"Country list: {countries}")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Line chart -- best for showing diverging emissions
          trajectories over time among the top emitters
        - **Country selection**: The 11 largest CO2 emitters by fuel combustion,
          covering a wide range of economies and development stages
        - **Time range**: 2000-2022, capturing China's dramatic rise and the
          relative plateaus or declines of mature economies
        - **Highlights**: China's emissions grew roughly 12x from 2000 levels,
          while the United States and Europe saw modest declines;
          India and Indonesia show steady upward trends
        """
    )
    return


@app.cell
def _(json, filtered):
    name_map = {
        "United States of America": "United States",
        "Russian Federation": "Russia",
        "Republic of Korea": "South Korea",
        "Iran (Islamic Republic of)": "Iran",
    }
    chart_data = [
        {"n": name_map.get(d["countryName"], d["countryName"]), "y": d["year"], "v": round(d["value"] * 100) / 100}
        for d in filtered
    ]
    chart_data.sort(key=lambda r: (r["y"], -r["v"]))
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
