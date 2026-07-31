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
        # Manufactures Exports Share — Methodology

        Slope chart showing manufactures as % of merchandise exports in 1990 vs 2022.
        The story: some countries have deepened industrial capacity while others
        (especially commodity exporters) have seen manufactures shrink as a share.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--TX-VAL-MANF-ZS-UN.json"
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
        return not any(w in name.lower() for w in agg_words)

    by_c = {}
    for row in data:
        cc = row['country']; cn = row['countryName']
        if not is_real(cn): continue
        yr = row['year']; val = row['value']
        if val is None: continue
        if cc not in by_c: by_c[cc] = {'name': cn, 'data': {}}
        by_c[cc]['data'][yr] = val

    selected_ccs = ['CN','JP','KR','DE','IT','IE','JO','HU','BR','CA','FI','IN','ID','GR','FR']
    result = []
    for cc in selected_ccs:
        if cc not in by_c: continue
        info = by_c[cc]
        a_yr = next((yr for yr in [1990,1991,1992] if yr in info['data']), None)
        b_yr = next((yr for yr in [2022,2021,2020] if yr in info['data']), None)
        if a_yr and b_yr:
            result.append({'n': info['name'], 'a': round(info['data'][a_yr],1), 'b': round(info['data'][b_yr],1)})
            print(f"{info['name']}: {info['data'][a_yr]:.1f} ({a_yr}) -> {info['data'][b_yr]:.1f} ({b_yr})")
    return a_yr, b_yr, by_c, is_real, result, selected_ccs


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
