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
        # Population Density — Methodology

        Horizontal bar chart showing the 20 most densely populated countries in 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-POP-DNST.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_names = {
        'Gibraltar', 'Bermuda', 'Aruba', 'Curacao', 'Guam', 'Cayman Islands',
        'Sint Maarten (Dutch part)', 'Turks and Caicos Islands', 'British Virgin Islands',
        'Channel Islands', 'Isle of Man', 'Faroe Islands', 'Macao SAR, China',
        'Monaco', 'Liechtenstein', 'San Marino', 'Andorra', 'Nauru', 'Tuvalu',
        'American Samoa', 'Northern Mariana Islands', 'Virgin Islands (U.S.)',
        'Puerto Rico', 'New Caledonia', 'French Polynesia'
    }
    skip_kw = [
        'area', ' countries', 'states', 'world', 'income', 'dividend', 'ifc', 'ibrd',
        'ida ', 'oecd', 'developing', 'least', 'heavily', 'south asia', 'middle east',
        'sub-saharan', 'latin', 'north america', 'east asia', 'euro area', 'european union',
        'post-', 'early-', 'late-', 'fragile', 'small state', 'hipc', 'opec',
        'arab world', 'g20', 'g-20', 'demographic', 'classification', 'caribbean small',
        'central europe', 'africa eastern', 'africa western', 'central african'
    ]
    def is_country(name):
        if name in skip_names:
            return False
        nl = name.lower()
        return not any(s in nl for s in skip_kw)

    pts_2023 = [x for x in data if x['year'] == 2023 and x['value'] is not None and is_country(x['countryName'])]
    pts_2023.sort(key=lambda x: -x['value'])
    top20 = pts_2023[:20]
    print(f"Top 20 densest countries: {[x['countryName'] for x in top20]}")
    return is_country, pts_2023, skip_kw, skip_names, top20


@app.cell
def _(json, top20):
    chart_data = [{"n": x['countryName'], "v": round(x['value'], 1)} for x in top20]
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
