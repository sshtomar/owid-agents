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
        # Scientific Journal Articles — Methodology

        Trend lines for top 10 countries by article count, 1996–2023.
        Values expressed in thousands.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-JRN-ARTC-SC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_keywords = ['World', 'Africa', 'Asia', 'Europe', 'America', 'Pacific', 'income',
                        'OECD', 'IBRD', 'IDA', 'Euro area', 'dividend', 'Caribbean',
                        'Central Europe', 'Fragile', 'HIPC', 'Heavily', 'Latin', 'Middle East',
                        'South Asia', 'Sub-Saharan', 'small states', 'all income', 'blend',
                        'only', 'total', 'Arab World', 'countries', 'Union', 'lending',
                        'Least', 'developing', 'emerging', 'States']
    def is_country(name):
        for kw in exclude_keywords:
            if kw.lower() in name.lower():
                return False
        return True

    countries = {}
    for pt in data:
        c = pt['countryName']
        if is_country(c) and pt['value'] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][pt['year']] = pt['value']

    latest_vals = {}
    for c, years in countries.items():
        for y in [2023, 2022, 2021]:
            if y in years:
                latest_vals[c] = years[y]
                break

    top10 = sorted(latest_vals.items(), key=lambda x: -x[1])[:10]
    print("Top 10 by recent publications:")
    for c, v in top10:
        print(f"  {c}: {v:,.0f}")
    return countries, is_country, latest_vals, top10


@app.cell
def _(countries, json, top10):
    chart_data = []
    for c, _ in top10:
        pts = sorted(countries[c].items())
        display = c.replace('Korea, Rep.', 'South Korea').replace('Iran, Islamic Rep.', 'Iran')
        s = [round(v / 1000, 1) for y, v in pts]
        chart_data.append({"n": display, "s": s, "y0": pts[0][0], "step": 1})

    print(f"Chart data: {len(chart_data)} series")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
