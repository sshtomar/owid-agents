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
        # International Tourism Arrivals — Methodology

        Shows how COVID-19 erased decades of tourism growth in a single year across
        the world's top destination countries.
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
    agg_words = ['income', 'region', 'world', 'area', 'europe', 'america', 'africa', 'asia',
                 'pacific', 'caribbean', 'dividend', 'ida', 'ibrd', 'oecd', 'union',
                 'countries', 'small states', 'average', 'total', 'developing', 'blend',
                 'heavily', 'fragile', 'saharan', 'eastern and', 'western and',
                 'north america', 'euro area', 'latin america', 'sub-saharan',
                 'middle east', 'south asia', 'east asia']

    def is_real(name):
        name_lower = name.lower()
        return not any(w in name_lower for w in agg_words)

    by_c = {}
    for row in data:
        cc = row['country']; cn = row['countryName']
        if not is_real(cn): continue
        yr = row['year']; val = row['value']
        if val is None: continue
        if cc not in by_c: by_c[cc] = {'name': cn, 'data': {}}
        by_c[cc]['data'][yr] = val

    tops = [(cc, info) for cc, info in by_c.items() if 2019 in info['data'] and 2020 in info['data']]
    tops.sort(key=lambda x: -x[1]['data'][2019])
    selected = tops[:10]
    print(f"Selected {len(selected)} countries")
    for cc, info in selected:
        v19 = info['data'].get(2019, 0)
        v20 = info['data'].get(2020, 0)
        print(f"  {info['name']}: 2019={v19/1e6:.1f}M 2020={v20/1e6:.1f}M ({(v20/v19-1)*100:.0f}%)")
    return by_c, selected, is_real


@app.cell
def _(json, selected):
    series = []
    for cc, info in selected:
        pts = []
        for yr in range(1995, 2021):
            if yr in info['data']:
                pts.append({'y': yr, 'v': round(info['data'][yr] / 1e6, 2)})
        series.append({'n': info['name'], 'pts': pts})
    print(json.dumps(series, separators=(',', ':')))
    return (series,)


if __name__ == "__main__":
    app.run()
