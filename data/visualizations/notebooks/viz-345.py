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
        # The Graying Planet — Methodology

        Trend lines showing the share of population aged 65 and above (%) from 1970 to 2024
        for eight major economies.
        Dataset: wb--SP-POP-65UP-TO-ZS (World Bank, 1960-2024, 153 countries)
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-65UP-TO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    countries = ['Japan', 'Italy', 'Germany', 'China', 'Brazil', 'India', 'Korea, Rep.', 'France']
    rows = [r for r in data if r['value'] is not None and r['country'] and len(r['country']) == 2
            and r['countryName'] in countries and r['year'] >= 1970]
    by_country = {}
    for r in rows:
        if r['countryName'] not in by_country:
            by_country[r['countryName']] = []
        by_country[r['countryName']].append((r['year'], round(r['value'], 2)))
    chart_data = []
    for c in countries:
        if c in by_country:
            pts = sorted(by_country[c])
            chart_data.append({'n': c, 's': [v for _, v in pts], 'y0': pts[0][0]})
    return (chart_data,)


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
