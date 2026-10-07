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
        # Asia's Poverty Exit — Methodology

        Documents the data pipeline for viz-367: share of population below
        $4.20/day (2021 PPP), earliest available vs. most recent.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-POV-LMIC.json"
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

    interesting = ['China','India','Indonesia','Bangladesh','Ethiopia','Ghana',
                   'Kenya','Honduras','Colombia','Brazil','Bolivia']
    pairs = []
    for c in interesting:
        rows = by_country.get(c, [])
        valid = sorted([(r['year'], r['value']) for r in rows if r['value'] is not None])
        if len(valid) < 2:
            continue
        early = next(((yr, v) for yr, v in valid if 1995 <= yr <= 2010), None)
        if not early:
            early = valid[0] if valid else None
        recent = valid[-1]
        if early and recent and early[0] != recent[0]:
            pairs.append({'n': c, 'y1': early[0], 'a': round(early[1], 1),
                          'y2': recent[0], 'b': round(recent[1], 1)})

    pairs.sort(key=lambda x: x['a'], reverse=True)
    print(f"Found {len(pairs)} countries")
    for p in pairs:
        drop = p['a'] - p['b']
        print(f"  {p['n']} ({p['y1']}-{p['y2']}): {p['a']:.1f}% -> {p['b']:.1f}% (drop: {drop:.1f} pp)")
    return by_country, interesting, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — different start years for different countries, but two-point
          comparison still shows direction and magnitude of change clearly
        - **Country selection**: Asia's success stories (China, India, Indonesia, Bangladesh),
          African countries at different stages (Ethiopia, Ghana, Kenya), and Latin America (Brazil, Colombia)
        - **Color**: Orange = >60 pp drop (extraordinary); amber = 40–60 pp; yellow = 15–40 pp; cool = slow/rising
        - **Story**: China's 79.4 pp reduction is the largest single-country poverty exit in recorded history.
          Kenya's rise from 51% to 66% shows that growth without equity can worsen outcomes.
        - **Note**: Years vary by data availability — interpret as multi-decade change, not fixed period
        """
    )
    return


@app.cell
def _(json, pairs):
    chart_data = [{'n': p['n'], 'a': p['a'], 'b': p['b'], 'ya': p['y1'], 'yb': p['y2']}
                  for p in pairs]
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
