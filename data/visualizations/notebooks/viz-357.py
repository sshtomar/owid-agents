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
    # Age Dependency Ratio, 1960–2024 — Methodology

    Documents data pipeline and editorial decisions for viz-357.
    """)
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
    target_countries = [
        'Chad', 'Angola', 'Burkina Faso',
        'India', 'Bangladesh', 'Indonesia',
        'Brazil', 'China',
        'Korea, Rep.', 'Japan',
        'Germany', 'Italy', 'France'
    ]
    selected_years = list(range(1960, 2025, 5))
    country_data = {}
    for r in data:
        n = r['countryName']
        if n in target_countries and r['value'] is not None:
            country_data.setdefault(n, {})[r['year']] = round(r['value'], 1)

    result = []
    for c in target_countries:
        pts = country_data.get(c, {})
        if not pts:
            continue
        series = [pts.get(yr) for yr in selected_years]
        while series and series[-1] is None:
            series.pop()
        result.append({'n': c, 's': series, 'y0': 1960, 'step': 5})

    print(f"Series count: {len(result)}")
    return result, target_countries, selected_years, country_data


@app.cell
def _(result):
    all_vals = [v for d in result for v in d['s'] if v is not None]
    print(f"Value range: {min(all_vals):.1f} - {max(all_vals):.1f}")
    countries = [d['n'] for d in result]
    years_covered = [1960 + i * 5 for i in range(max(len(d['s']) for d in result))]
    print(f"Countries: {countries}")
    print(f"Years: {years_covered[0]} - {years_covered[-1]}")
    return all_vals, countries, years_covered


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — shows divergent demographic trajectories over 64 years
    - **Country selection**: 3 Sub-Saharan Africa (persistently high), 3 South/SE Asia (declining), 2 Latin America/China (large decline), 2 East Asian (U-shaped aging), 3 Europe (slow U-shape)
    - **Time range**: 1960–2024 at 5-year intervals to cover full demographic transition period
    - **Story**: Sub-Saharan Africa never entered the demographic dividend; Asia and Latin America are mid-transition; East Asia and Europe now face rising old-age dependency
    - **Colors**: warm tones for Africa, cool blues for Asia, greens/muted for Europe
    """)
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
