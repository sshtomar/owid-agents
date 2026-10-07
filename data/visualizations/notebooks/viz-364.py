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
        # The Epidemiological Transition — Methodology

        Documents the data pipeline for viz-364: NCD deaths as % of total deaths,
        2000 vs. 2019.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DTH-NCOM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    print(f"Year range: {min(d['year'] for d in data)}-{max(d['year'] for d in data)}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    SKIP = ['income','World','states','dividend','Pacific','Atlantic','Caribbean',
            'Middle East','Arab','Euro area','Sub-Saharan','OECD','Fragile','Heavily',
            'Least','Low','Upper','High','Middle','developing','emerging','Baltics',
            'South Asia','Latin','countries','Americas','Africa','Asia','Europe','America','IDA','IBRD','North America']

    by_country = defaultdict(list)
    for row in data:
        c = row.get('countryName', '')
        if not any(x in c for x in SKIP):
            by_country[c].append({'year': row['year'], 'value': row['value']})

    interesting = ['Germany','Japan','France','Australia','Canada','United States','China','Brazil',
                   'Turkey','India','Mexico','Indonesia','Nigeria','Ethiopia','Kenya','Ghana',
                   'Senegal','Bangladesh','Haiti','Uganda','Mozambique','Chad','Algeria',
                   'South Africa','Egypt, Arab Rep.','Thailand']
    pairs = []
    for c in interesting:
        rows = by_country.get(c, [])
        valid = {r['year']: r['value'] for r in rows if r['value'] is not None}
        v2000 = valid.get(2000) or valid.get(2001)
        v2019 = valid.get(2019) or valid.get(2018) or valid.get(2020)
        if v2000 and v2019:
            label = c.replace('Egypt, Arab Rep.', 'Egypt')
            pairs.append({'n': label, 'a': round(v2000, 1), 'b': round(v2019, 1)})

    pairs.sort(key=lambda x: x['b'], reverse=True)
    print(f"Found {len(pairs)} countries")
    for p in pairs:
        print(f"  {p['n']}: {p['a']:.1f}% -> {p['b']:.1f}% (+{p['b']-p['a']:.1f} pp)")
    return by_country, interesting, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points, reveals direction and speed of transition
        - **Country selection**: Covers the full spectrum from <25% (Chad) to >91% (Germany)
        - **Color**: Orange = >20 pp gain (fastest transitioning); cool = <3 pp (already transitioned)
        - **Story**: Wealthy nations are near the NCD ceiling; developing nations are rising fast
          as vaccines, sanitation, and antibiotics defeat infectious disease
        - **Notable**: China's 8.5 pp jump (81.7% → 90.2%) happened in 19 years
        """
    )
    return


@app.cell
def _(json, pairs):
    print(json.dumps(pairs, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
