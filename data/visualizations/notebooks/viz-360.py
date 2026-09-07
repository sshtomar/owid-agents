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
    # Demographic Transition in Motion — Methodology

    Sparkline grid of annual population growth rates (%) for 21 countries, 1961–2024.
    Shows universal slowing, with sub-Saharan Africa as the main exception and Japan/
    South Korea now in negative territory.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    aggregate_kw = ['World', 'income', 'region', 'OECD', 'Arab', 'Africa Eastern',
                    'Africa Western', 'Pacific', 'America', 'Caribbean', 'Central Europe',
                    'Sub-Saharan', 'Euro', 'Fragile', 'IDA', 'IBRD', 'dividend',
                    'Heavily', 'Not classified', 'states', 'countries', 'Middle East',
                    'South Asia', 'East Asia', 'Latin America', 'North America']
    country_data = defaultdict(dict)
    for row in data:
        name = row['countryName']
        if row['value'] is not None and not any(k in name for k in aggregate_kw):
            country_data[name][row['year']] = row['value']

    target_map = {
        'Nigeria': 'Nigeria', 'Ethiopia': 'Ethiopia', 'Kenya': 'Kenya',
        'India': 'India', 'Bangladesh': 'Bangladesh', 'Indonesia': 'Indonesia',
        'Brazil': 'Brazil', 'Mexico': 'Mexico', 'Iran, Islamic Rep.': 'Iran',
        'China': 'China', 'Japan': 'Japan', 'Korea, Rep.': 'South Korea',
        'Germany': 'Germany', 'Italy': 'Italy', 'France': 'France',
        'Canada': 'Canada', 'Australia': 'Australia', 'Argentina': 'Argentina',
        'Colombia': 'Colombia', 'Iraq': 'Iraq', 'Russian Federation': 'Russia'
    }
    result = []
    for actual, display in target_map.items():
        yd = country_data.get(actual, {})
        s = [round(yd[y], 2) if y in yd else None for y in range(1961, 2025)]
        result.append({'n': display, 's': s, 'y0': 1961})
    print(f"Built {len(result)} country series")
    return country_data, result, target_map


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
