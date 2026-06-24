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
        # Financial Account Ownership (2014 vs 2021) -- Methodology

        Slope chart comparing the share of adults (15+) with a bank or mobile-money
        account across 24 representative countries, contrasting 2014 and 2021 Findex survey waves.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FX-OWN-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {
        'Arab World','East Asia & Pacific','Euro area','Europe & Central Asia','World',
        'High income','Low income','Middle income','Latin America & Caribbean',
        'Central Europe and the Baltics','South Asia','Sub-Saharan Africa',
        'Africa Eastern and Southern','Africa Western and Central','Low & middle income',
        'OECD members','Other small states','Pacific island small states',
        'Caribbean small states','Fragile and conflict affected situations',
        'Heavily indebted poor countries (HIPC)','IDA only','IDA blend','IDA & IBRD total',
        'IBRD only','Upper middle income','Lower middle income','North America',
        'East Asia & Pacific (excluding high income)','Europe & Central Asia (excluding high income)',
        'Latin America & Caribbean (excluding high income)','Middle East & North Africa',
        'Middle East & North Africa (excluding high income)',
        'Sub-Saharan Africa (excluding high income)','IDA total','Not classified',
        'Early-demographic dividend','Late-demographic dividend','Pre-demographic dividend',
        'Post-demographic dividend','IDA & IBRD total','South Asia (IDA & IBRD)',
        'Sub-Saharan Africa (IDA & IBRD countries)','East Asia & Pacific (IDA & IBRD countries)',
        'Latin America & the Caribbean (IDA & IBRD countries)',
        'Middle East & North Africa (IDA & IBRD countries)',
        'Europe & Central Asia (IDA & IBRD countries)',
        'Least developed countries: UN classification',
        'Heavily indebted poor countries'
    }
    country_ts = {}
    for x in data:
        n = x['countryName']
        if n not in AGGREGATES and len(n) > 2 and x['value'] is not None:
            if n not in country_ts:
                country_ts[n] = {}
            country_ts[n][x['year']] = x['value']

    pairs = []
    for c, ts in country_ts.items():
        y2014 = ts.get(2014)
        y2021 = ts.get(2021)
        if y2014 is not None and y2021 is not None:
            pairs.append({'n': c, 'a': round(y2014, 1), 'b': round(y2021, 1)})

    pairs.sort(key=lambda x: x['b'])
    print(f"Countries with 2014 and 2021 data: {len(pairs)}")
    return AGGREGATES, country_ts, pairs


@app.cell
def _(pairs):
    # Design rationale: pick 24 countries spanning the full range
    # Include countries with biggest increases, plus stable high/low performers
    selected_names = {
        'Afghanistan', 'Iraq', 'Chad', 'Cambodia', 'Egypt, Arab Rep.',
        'Guatemala', 'Honduras', 'Bolivia', 'India', 'Nigeria',
        'Ghana', 'Vietnam', 'Colombia', 'Brazil', 'Mexico',
        'South Africa', 'Argentina', 'Turkey', 'China', 'Poland',
        'Russia', 'Sweden', 'Japan', 'United States'
    }
    chart_data = [p for p in pairs if p['n'] in selected_names]
    chart_data.sort(key=lambda x: x['b'])
    print(f"Selected {len(chart_data)} countries")
    for c in chart_data:
        delta = c['b'] - c['a']
        print(f"  {c['n']}: {c['a']} -> {c['b']} ({delta:+.1f}pp)")
    return chart_data, selected_names


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
