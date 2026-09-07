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
    # Nuclear Electricity: Diverging National Paths — Methodology

    Trend lines showing nuclear share of electricity production (%) for 9 countries,
    1990–2024. Story: Germany's deliberate phase-out, Japan's Fukushima cliff, France's
    dominant nuclear grid, and Czech Republic's quiet expansion.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    aggregate_kw = ['World', 'income', 'region', 'OECD', 'Arab', 'Africa Eastern',
                    'Africa Western', 'Europe', 'Pacific', 'America', 'Caribbean',
                    'Central Europe', 'Sub-Saharan', 'Euro', 'Fragile', 'IDA', 'IBRD',
                    'dividend', 'Heavily', 'Not classified', 'states', 'countries']
    country_data = defaultdict(dict)
    for row in data:
        name = row['countryName']
        if row['value'] is not None and not any(k in name for k in aggregate_kw):
            country_data[name][row['year']] = row['value']

    target_countries = {
        'France': 'France', 'Belgium': 'Belgium', 'Czechia': 'Czech Rep.',
        'Finland': 'Finland', 'Hungary': 'Hungary', 'Korea, Rep.': 'South Korea',
        'Canada': 'Canada', 'Japan': 'Japan', 'Germany': 'Germany'
    }
    result = []
    for actual, display in target_countries.items():
        yd = country_data.get(actual, {})
        pts = [{'y': y, 'v': round(v, 1)} for y in range(1990, 2025) if (v := yd.get(y)) is not None]
        if pts:
            result.append({'n': display, 'pts': pts})
    print(f"Built {len(result)} series")
    return country_data, result, target_countries


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
