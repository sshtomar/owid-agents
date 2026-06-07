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
        for eight major economies, illustrating the global demographic aging transition.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-65UP-TO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


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
    print(f"Countries: {[d['n'] for d in chart_data]}")
    print(f"Year range: {chart_data[0]['y0']} to {chart_data[0]['y0'] + len(chart_data[0]['s']) - 1}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — continuous time series shows the sustained pace of aging
        - **Country selection**: Mix of already-aged (Japan, Italy, Germany, France) and rapidly aging (Korea, China) and young (India, Brazil)
        - **Key story**: Japan's pace is unprecedented; South Korea is now aging even faster from a lower base
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
