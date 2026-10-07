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
        # The Bottom Fifth's Share of Income — Methodology

        Documents the data pipeline for viz-366: income share held by
        the lowest 20%, around 2000 vs. around 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-FRST-20.json"
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

    interesting = ['Denmark','Finland','Belgium','Czechia','Germany','France','Canada',
                   'Australia','India','Bangladesh','China','Indonesia','Brazil',
                   'Colombia','Honduras','Angola']
    pairs = []
    for c in interesting:
        rows = by_country.get(c, [])
        valid = sorted([(r['year'], r['value']) for r in rows if r['value'] is not None])
        if len(valid) < 2:
            continue
        early = next(((yr, v) for yr, v in valid if 1999 <= yr <= 2007), None)
        recent = next(((yr, v) for yr, v in reversed(valid) if yr >= 2018), None)
        if early and recent:
            pairs.append({'n': c, 'a': round(early[1], 1), 'b': round(recent[1], 1),
                          'ya': early[0], 'yb': recent[0]})

    pairs.sort(key=lambda x: x['b'], reverse=True)
    print(f"Found {len(pairs)} countries")
    for p in pairs:
        print(f"  {p['n']} ({p['ya']}-{p['yb']}): {p['a']:.1f}% -> {p['b']:.1f}%")
    return by_country, interesting, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares two nearby time points, reveals structural inequality
        - **Country selection**: Covers Nordic equality exemplars, European mid-range, Asian countries
          (India surprisingly equal), and Latin American outliers
        - **Color**: By average level — cool green = high share (equal); orange = low share (unequal)
        - **Story**: A 3x gap separates Nordic countries (9-10%) from Latin American countries (2-4%).
          India's 10% share challenges the narrative that only wealthy countries can achieve equality.
        - **Note**: Survey methods and years vary — treat as indicative, not strictly comparable
        """
    )
    return


@app.cell
def _(json, pairs):
    print(json.dumps(pairs, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
