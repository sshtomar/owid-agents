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
        # Renewable Energy Share of Total Final Consumption: 1990 vs. 2022 — Methodology

        This notebook documents the data pipeline behind viz-360.
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
    from collections import defaultdict
    selected = ['Denmark', 'Germany', 'Estonia', 'Finland', 'Italy', 'Greece', 'Iceland',
                'Indonesia', 'Bangladesh', 'Bolivia', 'El Salvador', 'Ghana',
                'Brazil', 'India', 'China', 'France']

    by_country = defaultdict(dict)
    for row in data:
        if row['value'] is not None and row['countryName'] in selected:
            by_country[row['countryName']][row['year']] = row['value']

    chart_data = []
    for c in selected:
        ydata = by_country[c]
        a = ydata.get(1990)
        b = ydata.get(2022) or ydata.get(2021)
        if a is not None and b is not None:
            chart_data.append({'n': c, 'a': round(a, 1), 'b': round(b, 1), 'chg': round(b - a, 1)})

    chart_data.sort(key=lambda x: x['b'], reverse=True)
    print(f"Countries: {len(chart_data)}")
    for item in chart_data:
        print(f"  {item['n']}: {item['a']}% -> {item['b']}%, change={item['chg']:+.1f}pp")
    return chart_data, by_country, selected, defaultdict


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point comparison best shows direction and magnitude of change
        - **Country selection**: 16 countries including European green-transition leaders + developing nations
        - **Time range**: 1990 baseline (pre-energy-transition) vs. 2022 (latest available)
        - **Key story**: The paradox — many developing countries had *high* renewable shares in 1990 (biomass/traditional energy) but *fell* as fossil fuels powered their economic growth. Europe deliberately increased from low baselines.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
