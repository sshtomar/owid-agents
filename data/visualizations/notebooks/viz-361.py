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
        # Crude Death Rate — Methodology

        Trend lines showing crude death rate (per 1,000 people) for selected
        countries, 1960–2024. The counterintuitive story: Japan and Germany's
        death rates are RISING because of population aging, while Ethiopia, India,
        and Kenya show dramatic declines.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-CDRT-IN.json"
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

    targets = ['JP', 'DE', 'CN', 'IN', 'ET', 'KE', 'BR', 'KR']
    selected = []
    for cc in targets:
        if cc not in by_c: continue
        pts = [{'y': yr, 'v': round(by_c[cc]['data'][yr], 1)}
               for yr in range(1960, 2025) if yr in by_c[cc]['data']]
        if pts:
            selected.append({'n': by_c[cc]['name'], 'pts': pts})
            print(f"{by_c[cc]['name']}: {pts[0]['v']} ({pts[0]['y']}) -> {pts[-1]['v']} ({pts[-1]['y']})")
    return by_c, is_real, selected, targets


@app.cell
def _(json, selected):
    print(json.dumps(selected, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
