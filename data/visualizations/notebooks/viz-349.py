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
        # COVID Tourism Collapse — Methodology

        Slope chart comparing 2019 (last pre-COVID year) vs 2020 (first COVID year)
        international tourist arrivals for major destinations.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregates = {
        'Africa Eastern and Southern','Africa Western and Central','Arab World',
        'Caribbean small states','Central Europe and the Baltics','Early-demographic dividend',
        'East Asia & Pacific','East Asia & Pacific (excluding high income)',
        'East Asia & Pacific (IDA & IBRD countries)','Euro area','Europe & Central Asia',
        'Europe & Central Asia (excluding high income)','Europe & Central Asia (IDA & IBRD countries)',
        'Fragile and conflict affected situations','Heavily indebted poor countries (HIPC)',
        'High income','IBRD only','IDA & IBRD total','IDA blend','IDA only','IDA total',
        'Late-demographic dividend','Latin America & Caribbean',
        'Latin America & Caribbean (excluding high income)',
        'Latin America & the Caribbean (IDA & IBRD countries)',
        'Least developed countries: UN classification','Low & middle income','Low income',
        'Lower middle income','Middle East & North Africa',
        'Middle East & North Africa (excluding high income)',
        'Middle East & North Africa (IDA & IBRD countries)','Middle income','North America',
        'Not classified','OECD members','Other small states','Pacific island small states',
        'Post-demographic dividend','Pre-demographic dividend','Small states','South Asia',
        'South Asia (IDA & IBRD)','Sub-Saharan Africa','Sub-Saharan Africa (excluding high income)',
        'Sub-Saharan Africa (IDA & IBRD countries)','Upper middle income','World',
        'European Union','Middle East, North Africa, Afghanistan & Pakistan',
        'Middle East, North Africa, Afghanistan & Pakistan (excluding high income)',
        'Middle East, North Africa, Afghanistan & Pakistan (IDA & IBRD)'
    }
    by_country_year = {}
    for row in data:
        if row['countryName'] not in aggregates and row['value'] is not None and row['year'] in (2019, 2020):
            key = row['countryName']
            if key not in by_country_year:
                by_country_year[key] = {}
            by_country_year[key][row['year']] = row['value']

    slope_data = [(name, vals[2019], vals[2020]) for name, vals in by_country_year.items()
                  if 2019 in vals and 2020 in vals and vals[2019] > 15e6]
    slope_data.sort(key=lambda x: -x[1])
    print(f"Countries with >15M arrivals in 2019: {len(slope_data)}")
    for name, a, b in slope_data:
        drop = (a - b) / a * 100
        print(f"  {name}: {a/1e6:.1f}M -> {b/1e6:.1f}M ({drop:.0f}% drop)")
    return aggregates, by_country_year, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points, dramatic drops visible as steep downward slopes
        - **Country selection**: 13 countries with >15M arrivals in 2019 (both left and right data available)
        - **Color**: Encodes % drop — darker red = bigger collapse; Japan and Korea lost 87-86%
        - **Story**: Every single top tourism destination lost 46-94% of visitors in 2020
        - **Note**: France (−46%) had partial border openings; Japan/Hong Kong were most severe
        """
    )
    return


@app.cell
def _(json, slope_data):
    chart_data = [
        {"n": name, "a": round(a/1e6, 1), "b": round(b/1e6, 1)}
        for name, a, b in slope_data
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
