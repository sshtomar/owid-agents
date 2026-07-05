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
        # Consumer Price Inflation, 2000–2024 — Methodology

        This notebook documents the data pipeline behind viz-357.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FP-CPI-TOTL-ZG.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    selected = ['Germany', 'Japan', 'Brazil', 'China', 'India', 'France', 'Ghana', 'Australia', 'Korea, Rep.', 'Indonesia']
    label_map = {'Korea, Rep.': 'South Korea'}

    by_country = defaultdict(dict)
    for row in data:
        if row['value'] is not None and row['countryName'] in selected and 2000 <= row['year'] <= 2024:
            by_country[row['countryName']][row['year']] = row['value']

    years = list(range(2000, 2025))
    chart_data = []
    for c in selected:
        pts = []
        for y in years:
            v = by_country[c].get(y)
            if v is not None:
                pts.append({'y': y, 'v': round(v, 2)})
        name = label_map.get(c, c)
        chart_data.append({'n': name, 'pts': pts})

    print(f"Countries: {len(chart_data)}")
    return chart_data, by_country, years, selected, label_map, defaultdict


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how inflation varied over time across economies
        - **Country selection**: 10 major economies spanning Europe, Asia, Americas, Africa
        - **Time range**: 2000–2024 captures the 2008 crisis, 2009 deflation, and 2021–2022 global surge
        - **Highlights**: Japan's persistent near-zero/negative inflation; Ghana's chronic high inflation; universal 2022 spike
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
