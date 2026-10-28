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
        # Factory or Finance? Industry Value Added — Methodology

        Slope chart comparing industry (including construction) as % of GDP
        in 2000 vs 2022 for 18 diverse countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_markers = [
        'income', 'OECD', 'IDA', 'IBRD', 'Arab', 'Fragile', 'Small',
        'Heavily', 'Least', 'Euro area', 'Monetary', 'economies', 'only',
        'zone', 'Union', 'Saharan', 'World', 'demographic', 'dividend',
        'Pacific', 'Africa', 'America', 'Asia', 'Europe', 'region',
        'Caribbean', 'South Asia', 'East Asia', 'North Africa',
        'Sub-Saharan', 'Latin', 'North America', 'countries', 'total',
        'states', 'Central'
    ]

    def is_country(name):
        return not any(a.lower() in name.lower() for a in agg_markers)

    by_country = {}
    for x in data:
        if x['value'] is not None and is_country(x['countryName']):
            cn = x['countryName']
            if cn not in by_country:
                by_country[cn] = {}
            by_country[cn][x['year']] = x['value']

    print(f"Country count with data: {len(by_country)}")
    return by_country, is_country


@app.cell
def _(by_country):
    selected = [
        'Guyana', 'Chad', 'Congo, Dem. Rep.', 'Cambodia', 'Ireland',
        'Bangladesh', 'Ethiopia', "Cote d'Ivoire", 'Indonesia',
        'Korea, Rep.', 'India', 'Germany', 'Italy', 'Brazil',
        'Japan', 'China', 'Finland', 'France'
    ]
    chart_data = []
    for name in selected:
        if name in by_country and 2000 in by_country[name] and 2022 in by_country[name]:
            disp = name.replace('Congo, Dem. Rep.', 'Congo, D.R.C.').replace('Korea, Rep.', 'Korea, Rep.')
            chart_data.append({
                'n': disp,
                'a': round(by_country[name][2000], 1),
                'b': round(by_country[name][2022], 1)
            })
    chart_data.sort(key=lambda x: -x['b'])
    print(f"Chart rows: {len(chart_data)}")
    for row in chart_data:
        print(f"  {row['n']}: {row['a']} -> {row['b']} ({row['b']-row['a']:+.1f}pp)")
    return chart_data, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points, many entities, shows direction of change
        - **Year selection**: 2000 vs 2022 — broad coverage across dataset
        - **Country selection**: Mix of deindustrializing (France, Japan, China) and
          industrializing (Bangladesh, Cambodia, Ethiopia); resource-driven outliers (Guyana, Chad)
        - **Color**: diverging warm/cool by change direction
        - **Highlights**: Guyana's oil-fueled jump is the most dramatic; French deindustrialization
          is sharp; Bangladesh and Cambodia show export-led garment industrialization
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
