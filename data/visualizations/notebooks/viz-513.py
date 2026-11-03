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
        # Urban Electrification Progress — Methodology

        This notebook documents the data pipeline behind viz-513.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-ACCS-UR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_names = ['Eastern', 'Western', 'South Asia', 'East Asia', 'Sub-Saharan',
                 'Arab World', 'Euro area', 'European Union', 'OECD', 'World', 'income',
                 'IDA', 'IBRD', 'Caribbean', 'Fragility', 'dividend', 'states',
                 'Latin America', 'Middle East', 'North America', 'Pacific', 'Saharan',
                 'Heavily indebted', 'Least developed', 'classification', 'FCV',
                 'Central Europe', 'Europe &']
    real = [r for r in data if r['value'] is not None and
            r['country'].isalpha() and len(r['country']) == 2 and
            not any(w in r['countryName'] for w in agg_names)]
    by_c = {}
    for r in real:
        by_c.setdefault(r['countryName'], {})[r['year']] = r['value']
    print(f"Countries: {len(by_c)}")
    return agg_names, by_c, real


@app.cell
def _(by_c):
    slope_data = []
    for c, ys in by_c.items():
        if min(ys.values()) < 85 and max(ys.keys()) >= 2020:
            earliest_yr = min(ys.keys())
            latest_yr = max(y for y in ys if y >= 2020)
            a = round(ys[earliest_yr], 1)
            b = round(ys[latest_yr], 1)
            slope_data.append({"n": c, "a": a, "b": b, "ay": earliest_yr, "by": latest_yr})
    slope_data.sort(key=lambda x: -(x['b'] - x['a']))
    print(f"Countries: {len(slope_data)}")
    for s in slope_data[:10]:
        print(f"  {s['n']}: {s['a']}% ({s['ay']}) -> {s['b']}% ({s['by']})")
    return (slope_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — before/after comparisons at two time points
        - **Country selection**: 18 countries where urban access was below 85% at some point
        - **Time range**: Earliest available year vs 2024 (varies by country)
        - **Color encoding**: Green = large gain (70pp+), orange/red = smaller gain
        - **Story**: Urban electrification has made dramatic strides; Botswana went from 17% to 97%
        """
    )
    return


@app.cell
def _(json, slope_data):
    out = slope_data[:18]
    print(json.dumps(out, separators=(",", ":")))
    return (out,)


if __name__ == "__main__":
    app.run()
