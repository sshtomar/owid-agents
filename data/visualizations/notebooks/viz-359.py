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
        # Energy Use per Capita — Methodology

        Trend lines showing total primary energy use per capita (kg oil equivalent)
        for a diverse set of countries, 1990–2021.
        Story: China's dramatic rise mirrors the West's plateau or decline;
        developing nations grow slowly from a very low base.
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

    targets = ['CA', 'DE', 'CN', 'BR', 'IN', 'BD', 'ID', 'EG']
    selected = []
    for cc in targets:
        if cc not in by_c: continue
        pts = [{'y': yr, 'v': round(by_c[cc]['data'][yr])}
               for yr in range(1990, 2022) if yr in by_c[cc]['data']]
        if pts:
            selected.append({'n': by_c[cc]['name'], 'pts': pts})
            print(f"{by_c[cc]['name']}: {pts[0]['v']} ({pts[0]['y']}) -> {pts[-1]['v']} ({pts[-1]['y']})")
    return by_c, selected, is_real, targets


@app.cell
def _(json, selected):
    print(json.dumps(selected, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
