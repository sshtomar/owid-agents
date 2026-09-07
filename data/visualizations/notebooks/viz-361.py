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
    # Intentional Homicides: 200-fold Differences Across Countries — Methodology

    Horizontal bar chart showing homicide rates (per 100,000 people) for the 15 highest
    and 15 lowest countries in the dataset, most recent year >= 2018. Jamaica at 49.4
    vs Bahrain at 0.2 — a 200-fold spread.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    aggregate_kw = ['World', 'income', 'region', 'OECD', 'Arab', 'Africa Eastern',
                    'Africa Western', 'Pacific', 'America', 'Caribbean', 'East',
                    'Central', 'South', 'North', 'Sub-Saharan', 'Euro', 'Fragile',
                    'IDA', 'IBRD', 'dividend', 'Heavily', 'Not classified', 'states', 'countries']
    country_data = defaultdict(dict)
    for row in data:
        name = row['countryName']
        if row['value'] is not None and not any(k in name for k in aggregate_kw):
            country_data[name][row['year']] = row['value']

    rename = {'Korea, Rep.': 'South Korea', 'Hong Kong SAR, China': 'Hong Kong', 'Bahamas, The': 'Bahamas'}
    latest = {}
    for name, yd in country_data.items():
        yr = max(yd.keys())
        if yr >= 2018:
            latest[rename.get(name, name)] = round(yd[yr], 2)

    sorted_items = sorted(latest.items(), key=lambda x: -x[1])
    top15 = [{'n': n, 'v': v} for n, v in sorted_items[:15]]
    bot15 = [{'n': n, 'v': v} for n, v in sorted_items[-15:]]
    print(f"Top 15 highest: {[x['n'] for x in top15]}")
    print(f"Top 15 lowest: {[x['n'] for x in bot15]}")
    return bot15, latest, rename, sorted_items, top15


@app.cell
def _(json, top15, bot15):
    result = top15 + bot15
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
