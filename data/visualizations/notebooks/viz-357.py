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
        # Clean Cooking Fuels Access (2000 vs 2023) — Methodology

        Slope chart comparing the share of population with access to clean fuels
        and technologies for cooking across countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-CFT-ACCS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    print(f"Year range: {meta['dateRange']['start']} - {meta['dateRange']['end']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {'XD','XM','XN','XO','XP','XQ','XJ','XT','XS','XR','OE','EU','ZH','ZG','ZF','ZI',
                  '1A','1W','4E','7E','8S','B8','ZT','ZJ','ZL','ZQ','ZU','V1','V2','V3','V4',
                  'XC','XE','XL','XU','XY','YI','W6','S3','S1','S2','S4','T4','T5','T6','T7',
                  'XF','XG','XI'}

    countries = {}
    for pt in data:
        code = pt['country']
        name = pt['countryName']
        year = pt['year']
        val = pt['value']
        if val is not None and len(code) == 2 and code.isalpha() and code not in AGGREGATES:
            if name not in countries:
                countries[name] = {}
            countries[name][year] = round(val, 1)

    pairs = []
    for name, years in countries.items():
        v2000 = years.get(2000)
        v2023 = years.get(2023) or years.get(2022)
        if v2000 is not None and v2023 is not None:
            pairs.append({'n': name, 'a': v2000, 'b': v2023})

    pairs.sort(key=lambda x: x['b'])
    print(f"Countries with 2000 and 2023 data: {len(pairs)}")
    print(f"Range in 2023: {pairs[0]['b']}% (Burundi) to {pairs[-1]['b']}% ({pairs[-1]['n']})")
    return pairs, countries, AGGREGATES


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparisons across many entities
        - **Country selection**: 23 countries spanning the full range from <1% (Burundi) to 100% (Andorra, Australia)
          to show the global divide in clean cooking access
        - **Time range**: 2000 vs 2023, capturing 23 years of progress
        - **Color encoding**: By 2023 access level — red for <20%, terra for 20-50%, amber for 50-80%, green for 80-100%
        - **Highlights**: Indonesia 6.7%→90.6%, India 22.7%→76.7%, Cambodia 3.4%→58% (dramatic improvements)
          vs. Burundi 0.3%→0.1% (virtually no progress)
        """
    )
    return


@app.cell
def _(json, pairs):
    name_map = {
        'Central African Republic': 'C. African Rep.',
        'Congo, Dem. Rep.': 'DR Congo',
        'Gambia, The': 'Gambia',
        'Antigua and Barbuda': 'Antigua & Barbuda',
    }
    low = [p for p in pairs if p['b'] < 15][:8]
    mid_low = [p for p in pairs if 15 <= p['b'] < 55][::2][:4]
    mid = [p for p in pairs if 55 <= p['b'] < 90][::2][:6]
    high = [p for p in pairs if 90 <= p['b'] < 100][:3]
    full = [p for p in pairs if p['b'] >= 100][:3]
    selected = sorted(low + mid_low + mid + high + full, key=lambda x: x['b'])
    chart_data = [{'n': name_map.get(p['n'], p['n']), 'a': p['a'], 'b': p['b']} for p in selected]
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
