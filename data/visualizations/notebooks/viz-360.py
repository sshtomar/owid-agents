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
    mo.md("""
    # Labor Productivity: GDP per Person Employed, 2000 vs 2022 — Methodology

    Documents data pipeline and editorial decisions for viz-360.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-GDP-PCAP-EM-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    name_map = {
        'Korea, Rep.': 'Korea',
        'Brunei Darussalam': 'Brunei',
    }
    target_names = [
        'Ireland', 'Brunei Darussalam', 'Germany', 'France', 'Guyana', 'Bahrain',
        'Korea, Rep.', 'Japan', 'Kazakhstan', 'Georgia', 'Armenia', 'China',
        'Brazil', 'Indonesia', 'India', 'Bangladesh', 'Haiti', 'Ethiopia'
    ]

    y2000 = {r['countryName']: r['value'] for r in data if r['year'] == 2000 and r.get('value') is not None}
    y2022 = {r['countryName']: r['value'] for r in data if r['year'] == 2022 and r.get('value') is not None}

    result = []
    for c in target_names:
        if c in y2000 and c in y2022:
            dn = name_map.get(c, c)
            result.append({'n': dn, 'a': round(y2000[c] / 1000, 1), 'b': round(y2022[c] / 1000, 1)})

    result.sort(key=lambda x: x['b'], reverse=True)
    print(f"Countries: {len(result)}")
    return result, target_names, y2000, y2022, name_map


@app.cell
def _(result):
    for d in result:
        pct = (d['b'] - d['a']) / d['a'] * 100
        print(f"{d['n']}: ${d['a']}k -> ${d['b']}k ({pct:+.0f}%)")
    return


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Slope chart — compare two specific time points across many entities
    - **Year pair**: 2000 vs 2022 — long enough to capture structural shifts, recent enough to be relevant
    - **Country selection**: Mix of fast-growing (China +453%, Guyana +339%, Georgia +324%), stable high-income (Germany, France, Japan), and declining resource economies (Brunei -28%, Bahrain -19%, Haiti -15%)
    - **Color encoding**: Change magnitude — orange/red for large gains, green for moderate, brown-red for declines
    - **Units**: Thousands of constant 2021 PPP dollars to enable cross-country comparison
    """)
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
