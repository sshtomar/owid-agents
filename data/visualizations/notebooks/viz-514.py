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
        # Electricity from Oil Sources -- Methodology

        Slope chart showing the share of electricity generated from oil/petroleum
        (% of total) for 15 high-oil-share countries, comparing 1990 to 2024.

        Oil-based electricity is expensive and carbon-intensive; many countries
        have been transitioning away while others remain stuck or have increased
        their oil dependency.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-PETR-ZS.json"
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
        if 1990 in years and 2024 in years:
            slope_data.append({'n': name, 'a': round(years[1990], 1), 'b': round(years[2024], 1)})

    slope_data.sort(key=lambda x: x['b'], reverse=True)
    chart_data = slope_data[:15]

    for d in chart_data:
        print(f"  {d['n']}: {d['a']}% -> {d['b']}% ({d['b']-d['a']:+.1f}pp)")
    return chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (1990 vs 2024)
        - **Country selection**: Top 15 by 2024 oil share in electricity mix
        - **Color**: By magnitude of reduction (green = switched away, red = stuck)
        - **Notable stories**:
          - Haiti INCREASED from 20% to 81% (crisis-driven reversal)
          - Honduras went from 1.7% to 47% (puzzling increase)
          - Jamaica, Dominican Republic, Benin dramatically reduced
          - Chad and Cuba remain almost entirely oil-based
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
