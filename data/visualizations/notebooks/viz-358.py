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
        # Renewable Energy Consumption Share -- Methodology

        Trend lines comparing renewable energy as % of total final energy consumption
        (1990-2021) for 10 selected countries. World Bank indicator EG.FEC.RNEW.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-FEC-RNEW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['Germany', 'Denmark', 'Finland', 'Italy', 'Iceland',
                'China', 'Brazil', 'India', 'Japan', 'Austria']
    filtered = [r for r in data if r["value"] is not None and r["countryName"] in selected]
    print(f"Filtered to {len(filtered)} rows for {len(set(r['countryName'] for r in filtered))} countries")
    return (filtered,)


@app.cell
def _(filtered):
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    values = [d["value"] for d in filtered]
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f}% - {max(values):.1f}%")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows trajectory of energy transition
        - **Country selection**: Mix of leaders (Iceland, Finland), fast movers (Denmark, Germany, Italy), and large economies (China, India, Brazil, Japan)
        - **Time range**: 1990-2021
        - **Highlights**: Iceland always high (geothermal/hydro), Denmark's rapid wind expansion, China's paradox of declining share
        """
    )
    return


@app.cell
def _(json, filtered):
    from collections import defaultdict
    series = defaultdict(dict)
    for r in filtered:
        series[r["countryName"]][r["year"]] = r["value"]
    chart_data = [
        {"n": name, "pts": [{"y": y, "v": round(v, 1)} for y, v in sorted(pts.items())]}
        for name, pts in series.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
