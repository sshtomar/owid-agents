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
        # Population at Coastal Risk (Below 5m Elevation) -- Methodology

        Horizontal bar chart of countries ranked by the share of their population
        living in areas below 5 meters elevation, using 2015 data.

        This metric serves as a proxy for sea-level-rise vulnerability: countries
        where large fractions of people live near sea level face catastrophic
        displacement risk as oceans rise.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-POP-EL5M-ZS.json"
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

    # Most recent value per country
    by_country = {}
    for d in filtered:
        name = d['countryName']
        if name not in by_country or d['year'] > by_country[name]['year']:
            by_country[name] = {'value': d['value'], 'year': d['year']}

    bar_data = [{'n': name, 'v': round(vals['value'], 1)} for name, vals in by_country.items()]
    bar_data.sort(key=lambda x: x['v'], reverse=True)
    chart_data = bar_data[:20]

    print("Top 20 by share of population below 5m elevation:")
    for d in chart_data:
        print(f"  {d['n']}: {d['v']}%")
    return chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart (single metric comparison)
        - **Country selection**: Top 20 by share of population below 5m elevation
        - **Color**: Warm sequential ramp (#EA5E33 -> #A6C4A2) by rank
        - **Highlights**:
          - Guyana (78%) is protected by colonial-era sea dykes -- much of the country
            is literally below sea level
          - Kiribati and other Pacific island nations face existential risk
          - Major economies (Japan, Egypt, Bangladesh) have large absolute exposed
            populations despite lower percentage shares
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
