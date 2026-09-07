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
    # The Global Higher Education Boom — Methodology

    Trend lines for tertiary school enrollment (% gross) by world region, 1999–2024.
    East Asia & Pacific surged from 15% to 63%. Sub-Saharan Africa remains at ~9%.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-TER-ENRR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    country_data = defaultdict(dict)
    for row in data:
        if row['value'] is not None:
            country_data[row['countryName']][row['year']] = row['value']

    regions = ['Sub-Saharan Africa', 'South Asia', 'East Asia & Pacific',
               'Europe & Central Asia', 'Latin America & Caribbean', 'North America', 'World']
    result = []
    for region in regions:
        yd = country_data.get(region, {})
        pts = [{'y': y, 'v': round(v, 1)} for y in range(1999, 2025) if (v := yd.get(y)) is not None]
        # Sub-Saharan Africa has data back to 1970 — include that context
        if region == 'Sub-Saharan Africa':
            extra = [{'y': y, 'v': round(v, 1)} for y in range(1970, 1999) if (v := yd.get(y)) is not None]
            pts = extra + pts
        if pts:
            result.append({'n': region, 'pts': pts})
    print(f"Built {len(result)} region series")
    return country_data, result, regions


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
