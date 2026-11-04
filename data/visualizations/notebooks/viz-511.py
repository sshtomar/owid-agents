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
        # Low-Birthweight Babies -- Methodology

        Slope chart of low-birthweight rate (% of births) for 20 high-burden
        countries, comparing 2000 to 2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-BRTW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_keywords = [
        'World', 'income', 'region', 'developing', 'dividend', 'IBRD', 'IDA',
        'OECD', 'Europe', 'America', 'Pacific', 'Caribbean', 'East', 'South Asia',
        'North Africa', 'Sub-Saharan', 'Latin', 'Low', 'Middle', 'High', 'countries',
        'states', 'Euro', 'fragile', 'blend', 'only', 'Union', 'Group', 'West',
        'situations', 'FCV', 'Heavily', 'Arab World', 'Eastern and', 'Western and',
        'demographic', 'Central Europe', 'and Central', 'and Eastern', 'early', 'late'
    ]
    def is_aggregate(name):
        return any(kw.lower() in name.lower() for kw in agg_keywords)

    filtered = [d for d in data if not is_aggregate(d['countryName']) and d['value'] is not None]

    by_country = {}
    for d in filtered:
        name = d['countryName']
        if name not in by_country:
            by_country[name] = {}
        by_country[name][d['year']] = d['value']

    slope_data = []
    for name, years in by_country.items():
        if 2000 in years and 2020 in years:
            slope_data.append({'n': name, 'a': round(years[2000], 1), 'b': round(years[2020], 1)})

    slope_data.sort(key=lambda x: x['b'], reverse=True)
    chart_data = slope_data[:20]
    print(f"Countries with 2000+2020 data: {len(slope_data)}")
    print(f"Top 20 by 2020 value: {[(d['n'], d['b']) for d in chart_data[:5]]}")
    return chart_data, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows change between two specific points
        - **Country selection**: Top 20 by 2020 prevalence (highest burden countries)
        - **Time range**: 2000-2020 (2 decades of progress)
        - **Color**: Green for improvement, red for worsening
        - **Highlights**: India and Bangladesh show largest absolute reductions;
          Jordan and a few Caribbean nations show unexpected increases
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
