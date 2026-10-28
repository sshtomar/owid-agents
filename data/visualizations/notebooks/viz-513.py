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
        # Surplus or Deficit? Current Account Balance — Methodology

        Slope chart comparing current account balance (% of GDP) in 2000 vs 2022
        for 19 economies across different regions and income levels.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--BN-CAB-XOKA-GD-ZS.json"
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

    return by_country, is_country


@app.cell
def _(by_country, json):
    selected = [
        'Denmark', 'Germany', 'Australia', 'Israel', 'Japan', 'China',
        'Korea, Rep.', 'Canada', 'France', 'Italy', 'Brazil', 'India',
        'Argentina', 'Colombia', 'Chile', 'Bangladesh', 'Indonesia',
        'Hungary', 'Greece'
    ]

    chart_data = []
    for name in selected:
        if name in by_country and 2000 in by_country[name] and 2022 in by_country[name]:
            chart_data.append({
                'n': name,
                'a': round(by_country[name][2000], 1),
                'b': round(by_country[name][2022], 1)
            })

    print(f"Chart rows: {len(chart_data)}")
    for row in chart_data:
        print(f"  {row['n']}: {row['a']:+.1f}% -> {row['b']:+.1f}% ({row['b']-row['a']:+.1f}pp)")

    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, name, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two snapshots, reveals which economies improved or worsened
        - **Key story**: Denmark went from +1.4% to +11.2% (biggest surplus gain);
          Chile fell from -1.1% to -8.9%; Germany flipped from modest deficit to +4.1%
        - **Reference line**: 0% baseline marks balanced vs surplus/deficit
        """
    )
    return


if __name__ == "__main__":
    app.run()
