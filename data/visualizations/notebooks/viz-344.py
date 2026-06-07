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
        # Infant Mortality: Thirty Years of Progress — Methodology

        Slope chart comparing infant mortality rates (deaths in first year per 1,000 live births)
        in 1990 vs 2022 for the 15 countries with the highest rates in 1990.
        Dataset: wb--SP-DYN-IMRT-IN (World Bank, 1960-2024, 140 countries)
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-IMRT-IN.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    exclude_kw = ['IDA', 'IBRD', 'Sub-Saharan', 'Least developed', 'Heavily indebted', 'Low income',
                  'Africa Eastern', 'Africa Western', 'dividend', 'Fragile', 'World',
                  'East Asia', 'South Asia', 'Latin America', 'Middle East', 'Europe', 'Central Asia',
                  'Arab World', 'Caribbean', 'Pacific', 'North America', 'OECD', 'Euro area']
    rows = [r for r in data if r['value'] is not None and r['country'] and len(r['country']) == 2
            and not any(kw.lower() in r['countryName'].lower() for kw in exclude_kw)]
    by_country = {}
    for r in rows:
        c = r['countryName']
        if c not in by_country:
            by_country[c] = {}
        by_country[c][r['year']] = r['value']
    slope_data = [{'n': c, 'p': round(y[1990], 1), 'q': round(y[2022], 1)}
                  for c, y in by_country.items() if 1990 in y and 2022 in y]
    slope_data.sort(key=lambda x: x['p'], reverse=True)
    chart_data = slope_data[:15]
    print(f"Top 15 countries by 1990 rate selected")
    return (chart_data,)


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
