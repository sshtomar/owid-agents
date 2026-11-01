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
        # PM2.5 Exposure Above WHO Guidelines -- Methodology

        This notebook documents the data pipeline for the trend lines chart
        showing the share of national populations exposed to PM2.5 concentrations
        exceeding the WHO annual guideline value (10 micrograms per cubic meter).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-ATM-PM25-MC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    all_years = sorted(set(r["year"] for r in data))
    print(f"Years available: {all_years}")

    country_years = {}
    for r in data:
        c = r["countryName"]
        if c not in country_years:
            country_years[c] = {}
        country_years[c][r["year"]] = round(r["value"], 2)
    print(f"Total entries: {len(country_years)}")
    return all_years, country_years


@app.cell
def _(mo):
    mo.md(
        """
        ## Country Selection

        Selected 11 countries spanning the full range of trajectories:
        - Finland, Canada, Ireland: early/fast cleaners (now near 0%)
        - Denmark, Andorra, Japan, France: gradual improvers
        - Germany, Austria, Brazil: modest improvers still above 80%

        Each tells a different story about air-quality policy progress.
        """
    )
    return


@app.cell
def _(all_years, country_years, json):
    SELECTED = [
        "Finland", "Canada", "Ireland", "Australia",
        "Denmark", "Andorra", "France", "Japan",
        "Germany", "Austria", "Brazil"
    ]

    chart_data = []
    for c in SELECTED:
        if c in country_years:
            yd = country_years[c]
            pts = [{"y": yr, "v": yd[yr]} for yr in all_years if yr in yd]
            chart_data.append({"n": c, "pts": pts})

    print(f"Chart series: {len(chart_data)}")
    for s in chart_data:
        first = s["pts"][0]["v"]
        last = s["pts"][-1]["v"]
        print(f"  {s['n']}: {first} -> {last}")

    print()
    print("JSON:")
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
