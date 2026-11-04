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
        # Lifetime Risk of Maternal Death -- Methodology

        Slope chart of lifetime risk of dying from maternal causes (%) for 20
        high-burden countries, 1990 vs 2023. Lifetime risk is the cumulative
        probability across all pregnancies a woman is likely to have, making it
        more personally relatable than the per-100,000 births ratio.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MMR-RISK-ZS.json"
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

    slope_data = []
    for name, years in by_country.items():
        if 1990 in years and 2023 in years:
            slope_data.append({'n': name, 'a': round(years[1990], 3), 'b': round(years[2023], 3)})

    slope_data.sort(key=lambda x: x['b'], reverse=True)
    chart_data = slope_data[:20]
    vals_a = [d['a'] for d in chart_data]
    vals_b = [d['b'] for d in chart_data]
    print(f"1990 range: {min(vals_a):.3f} to {max(vals_a):.3f}%")
    print(f"2023 range: {min(vals_b):.3f} to {max(vals_b):.3f}%")
    return chart_data, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows change between two specific years
        - **Country selection**: Top 20 by 2023 lifetime risk (highest burden)
        - **Color**: Warm-to-cool ramp by pct improvement (% decline from 1990)
        - **Highlights**: Afghanistan improved from 10.7% to 2.5%; CAR and Chad still
          face lifetime risks above 4% (1 in 24 chance)
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
