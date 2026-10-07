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
        # Two Decades of Energy Divergence — Methodology

        Documents the data pipeline for viz-363: energy use per capita
        (kg of oil equivalent), 2000 vs. 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    SKIP = ['income','World','states','dividend','Pacific','Atlantic','Caribbean',
            'Middle East','Arab','Euro area','Sub-Saharan','OECD','Fragile','Heavily',
            'Least','Low','Upper','High','Middle','developing','emerging','Baltics',
            'South Asia','Latin','countries','Americas','Africa','Asia','Europe','America','IDA','IBRD']

    by_country = defaultdict(list)
    for row in data:
        c = row.get('countryName', '')
        if not any(x in c for x in SKIP):
            by_country[c].append({'year': row['year'], 'value': row['value']})

    interesting = ['United States','Canada','Australia','Germany','France','Japan',
                   'Korea, Rep.','China','India','Brazil','Indonesia','Mexico',
                   'Nigeria','Ethiopia','Bangladesh','Saudi Arabia','Iran, Islamic Rep.',
                   'Kazakhstan','South Africa','Turkey','Argentina','Poland','Ukraine']
    pairs = []
    for c in interesting:
        rows = by_country.get(c, [])
        valid = {r['year']: r['value'] for r in rows if r['value'] is not None}
        v2000 = valid.get(2000)
        v2022 = valid.get(2022) or valid.get(2021)
        if v2000 and v2022:
            label = c.replace('Korea, Rep.', 'South Korea').replace('Iran, Islamic Rep.', 'Iran')
            pairs.append({'n': label, 'a': round(v2000), 'b': round(v2022)})

    pairs.sort(key=lambda x: x['b'], reverse=True)
    print(f"Found {len(pairs)} countries with data")
    for p in pairs:
        pct = round((p['b'] - p['a']) / p['a'] * 100)
        print(f"  {p['n']}: {p['a']:,} -> {p['b']:,} kg ({pct:+d}%)")
    return by_country, interesting, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares two time points, shows direction and magnitude
        - **Country selection**: Mix of highest consumers, fastest growers, and low-income countries
        - **Color**: Orange = tripled (>150% growth); amber = >40% growth; yellow = modest growth; cool = declined
        - **Story**: Energy efficiency gains in rich nations contrast with China's 3x surge and
          continued extreme low use in Bangladesh, Ethiopia — showing the scale of the energy gap
        - **Scale**: 0 to 9,000 kg to include Canada's high baseline
        """
    )
    return


@app.cell
def _(json, pairs):
    print(json.dumps(pairs, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
