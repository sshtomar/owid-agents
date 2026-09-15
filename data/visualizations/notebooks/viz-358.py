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
    mo.md("""
    # Energy Use per Capita, 1990–2022 — Methodology

    Documents data pipeline and editorial decisions for viz-358.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target_countries = [
        'Iceland', 'Canada', 'Korea, Rep.', 'Germany',
        'China', 'Iran, Islamic Rep.', 'Brazil',
        'India', 'Indonesia', 'Bangladesh', 'Chad', 'Ethiopia',
    ]
    selected_years = list(range(1990, 2023, 2))
    country_data = {}
    for r in data:
        n = r['countryName']
        display_name = 'Iran' if n == 'Iran, Islamic Rep.' else n
        if n in target_countries and r.get('value') is not None:
            country_data.setdefault(display_name, {})[r['year']] = round(r['value'], 0)

    result = []
    for c in target_countries:
        dn = 'Iran' if c == 'Iran, Islamic Rep.' else c
        pts = country_data.get(dn, {})
        if not pts:
            continue
        series = [pts.get(yr) for yr in selected_years]
        while series and series[-1] is None:
            series.pop()
        result.append({'n': dn, 's': series, 'y0': 1990, 'step': 2})

    print(f"Series count: {len(result)}")
    return result, target_countries, selected_years, country_data


@app.cell
def _(result):
    all_vals = [v for d in result for v in d['s'] if v is not None]
    print(f"Value range: {min(all_vals):.0f} - {max(all_vals):.0f} kg oil eq per capita")
    return (all_vals,)


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — reveals divergent energy trajectories since 1990
    - **Country selection**: Iceland (geothermal outlier), Canada (high per-capita), Korea (dramatic rise), Germany (efficiency decline), China (rapid growth), Iran (rising), Brazil (moderate), India/Indonesia (rising low), Bangladesh/Chad/Ethiopia (very low)
    - **Time range**: 1990–2022 at 2-year intervals (data available from 1990)
    - **Story**: A 40x gap separates Iceland from Chad. China nearly tripled energy use; many low-income countries remain stuck below 400 kg despite economic growth
    - **Y-axis**: Linear scale to show full magnitude of the gap
    """)
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
