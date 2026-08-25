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
        # Anemia Among Women of Reproductive Age — Methodology

        Documents the data pipeline behind viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-ALLW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x['value'] is not None:
            by_country[x['countryName']][x['year']] = x['value']
    agg_words = [
        'Africa', 'Asia', 'Europe', 'America', 'Caribbean', 'Pacific',
        'Middle East', 'World', 'OECD', 'IDA', 'IBRD', 'income', 'states',
        'dividend', 'Arab', 'South Asia', 'Latin', 'Sub-Saharan', 'East Asia',
        'Central', 'North Africa', 'Least developed', 'Heavily', 'HIPC',
        'UN classification', 'Channel', 'Islands', 'developing', 'emerging', 'Euro'
    ]
    countries = {c: v for c, v in by_country.items() if not any(w in c for w in agg_words)}
    slope_data = []
    for c, v in countries.items():
        a = v.get(2000)
        b = v.get(2022) or v.get(2021) or v.get(2023)
        if a and b:
            slope_data.append({"n": c, "a": round(a, 1), "b": round(b, 1)})
    slope_data.sort(key=lambda x: x['b'], reverse=True)
    top20 = slope_data[:20]
    for s in top20:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f})")
    return by_country, countries, slope_data, top20


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — 2000 vs 2022 prevalence for the 20 highest-burden countries
        - **Key finding**: Anemia remains stubbornly high in West and Central Africa; India
          is the most populous high-burden country and has worsened slightly; Afghanistan
          increased significantly (+13 pp); many countries show modest improvement
        - **Color encoding**: Warm tones for worsening; cool green for improvement
        """
    )
    return


@app.cell
def _(json, top20):
    name_map = {
        "Cote d'Ivoire": "Côte d'Ivoire",
        "Congo, Rep.": "Congo",
        "Congo, Dem. Rep.": "DR Congo",
        "Gambia, The": "Gambia",
    }
    for s in top20:
        s['n'] = name_map.get(s['n'], s['n'])
    print(json.dumps(top20, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
