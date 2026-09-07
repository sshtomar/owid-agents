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
    # Conservation Gains: Terrestrial Protected Areas 2013 vs 2023 — Methodology

    Slope chart comparing terrestrial protected areas (% of total land) between 2013
    and 2023 for 21 countries. Highlights dramatic increases in Croatia, Bahamas, Bhutan.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-LND-PTLD-ZS.json"
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

    rename = {'Korea, Rep.': 'South Korea', 'Bahamas, The': 'Bahamas'}
    slope_data = []
    for name, yd in country_data.items():
        a = yd.get(2013)
        b = yd.get(2023) or yd.get(2022)
        if a is not None and b is not None:
            slope_data.append({'n': rename.get(name, name), 'a': round(a, 1), 'b': round(b, 1)})

    picks = {'Croatia', 'Bahamas', 'Bhutan', 'Cyprus', 'Cambodia', 'Japan', 'South Korea',
             'Bolivia', 'Germany', 'Bulgaria', 'Belize', 'Greece', 'Australia', 'Brazil',
             'France', 'Canada', 'Kenya', 'India', 'China', 'Colombia', 'Ecuador'}
    result = [x for x in slope_data if x['n'] in picks]
    result.sort(key=lambda x: -(x['b'] - x['a']))
    print(f"Countries: {len(result)}")
    for x in result:
        print(f"  {x['n']}: {x['a']} -> {x['b']}")
    return result, slope_data


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
