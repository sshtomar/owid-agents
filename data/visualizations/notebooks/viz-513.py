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
        # Female Tobacco Use Prevalence -- Methodology

        Trend lines for selected countries showing female smoking rates from
        2000 to 2024. The chart reveals stark regional contrasts: Balkan
        countries rising, South/Southeast Asia and Latin America falling sharply.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-PRV-SMOK-FE.json"
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
        'situations', 'FCV', 'Arab World', 'Eastern and', 'Western and',
        'demographic', 'Central Europe', 'and Central', 'and Eastern'
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

    selected = [
        'Bulgaria', 'Croatia', 'France', 'Greece', 'Germany',
        'Chile', 'Brazil', 'Japan', 'China', 'India', 'Indonesia'
    ]

    years = list(range(2000, 2025))
    chart_data = []
    for name in selected:
        if name in by_country:
            pts = [{'y': y, 'v': round(by_country[name][y], 1)}
                   for y in years if y in by_country[name]]
            if pts:
                chart_data.append({'n': name, 'pts': pts})

    for t in sorted(chart_data, key=lambda x: x['pts'][-1]['v'], reverse=True):
        print(f"  {t['n']}: {t['pts'][0]['v']} -> {t['pts'][-1]['v']}")
    return chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Multi-series trend lines with endpoint labels
        - **Country selection**: 11 countries spanning 3 trajectory groups:
          rising (Balkans), falling fast (India, Chile, Greece), stable-low (China)
        - **Color**: Warm (rising/high) to cool (falling fast) diverging scheme
        - **Reference line**: 15% (approximate EU average) as context anchor
        - **Highlights**: India's rate fell from 40.7% to 9.7% over 24 years;
          Bulgaria and Croatia are heading in the opposite direction
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
