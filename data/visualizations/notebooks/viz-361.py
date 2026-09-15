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
    # School Life Expectancy, 1990 vs 2018 — Methodology

    Documents data pipeline and editorial decisions for viz-361.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-SCH-LIFE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude = ['income', 'dividend', 'World', 'Europe', 'Asia', 'Africa', 'America',
               'Caribbean', 'Arab', 'OECD', 'Fragile', 'HIPC', 'Small', 'Least',
               'IDA', 'IBRD', 'Post-', 'Pre-', 'Middle', 'Latin ', 'South Asia',
               'Global Partnership', 'Euro area', 'North America']

    y1990 = {r['countryName']: r['value'] for r in data if r['year'] == 1990 and r.get('value') is not None}
    y2018 = {r['countryName']: r['value'] for r in data if r['year'] == 2018 and r.get('value') is not None}

    common = set(y1990) & set(y2018)
    real = [n for n in common if not any(x in n for x in exclude)]

    result = [{'n': n, 'a': round(y1990[n], 1), 'b': round(y2018[n], 1)} for n in real]
    result.sort(key=lambda x: x['b'], reverse=True)
    print(f"Countries: {len(result)}")
    return result, y1990, y2018, common, real, exclude


@app.cell
def _(result):
    for d in result:
        gain = d['b'] - d['a']
        print(f"{d['n']}: {d['a']}yr -> {d['b']}yr (+{gain:.1f}yr)")
    return


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Slope chart — directly shows before/after for a named set of countries
    - **Year pair**: 1990 vs 2018 — widest span with reasonable country coverage (2019 has fewer)
    - **Country selection**: All 26 countries with data in both years (after removing regional aggregates)
    - **Color encoding**: Years gained — orange/red for large gains (Afghanistan +7.7, Ireland +7.4), green for moderate, pale for small
    - **Story**: Remarkable convergence — countries starting from 2–5 years added 6–8 years; those starting from 12+ years added 2–7 years. The gap narrowed but persists (9 vs 20 years)
    """)
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
