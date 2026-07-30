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
        # Adjusted Net National Income per Capita — Methodology

        Slope chart comparing adjusted net national income per capita (current USD)
        between 2000 and 2021 for 20 countries across the income spectrum.

        Unlike GDP, adjusted NNI subtracts consumption of fixed capital and adds
        net transfers from abroad, giving a better picture of sustainable national wealth.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-ADJ-NNTY-PC-CD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_kw = [
        'area', ' countries', 'states', 'world', 'income', 'dividend', 'ifc', 'ibrd',
        'ida ', 'oecd', 'developing', 'least', 'heavily', 'south asia', 'middle east',
        'sub-saharan', 'latin', 'north america', 'east asia', 'euro area', 'european union',
        'post-', 'early-', 'late-', 'fragile', 'small state', 'hipc', 'opec',
        'arab world', 'g20', 'g-20', 'demographic', 'classification', 'caribbean small',
        'central europe', 'africa eastern', 'africa western', 'central african',
        'europe & central', 'not classified', 'unclassified'
    ]
    skip_names = {'Channel Islands', 'Isle of Man', 'Faroe Islands'}

    def is_country(name):
        if name in skip_names:
            return False
        nl = name.lower()
        return not any(s in nl for s in skip_kw)

    by_country = {}
    for x in data:
        if is_country(x['countryName']) and x['value'] is not None and x['value'] > 0 and x['year'] in [2000, 2021]:
            if x['countryName'] not in by_country:
                by_country[x['countryName']] = {}
            by_country[x['countryName']][x['year']] = x['value']

    both = [(c, round(v[2000]), round(v[2021])) for c, v in by_country.items() if 2000 in v and 2021 in v]
    both.sort(key=lambda x: x[2], reverse=True)
    print(f"Countries: {len(both)}")
    return both, by_country, is_country, skip_kw, skip_names


@app.cell
def _(both, json):
    # Select 20 countries spread across the income spectrum
    target = both[:8] + both[len(both)//4:len(both)//4+4] + both[len(both)//2:len(both)//2+4] + both[-8:]
    target_unique = list({c: (a, b) for c, a, b in target}.items())
    target_unique.sort(key=lambda x: x[1][1], reverse=True)
    chart_data = [{"n": c, "a": a, "b": b} for c, (a, b) in target_unique[:20]]
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, target, target_unique


if __name__ == "__main__":
    app.run()
