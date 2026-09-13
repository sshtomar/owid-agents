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
        # Primary School Completion Rate — Methodology

        Slope chart comparing ~2000 vs latest year across 25 countries.
        Sorted by absolute improvement (percentage points gained).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_keywords = ['World', 'Africa', 'Asia', 'Europe', 'America', 'Pacific', 'income',
                        'OECD', 'IBRD', 'IDA', 'Euro area', 'dividend', 'Caribbean',
                        'Central Europe', 'Fragile', 'HIPC', 'Heavily', 'Latin', 'Middle East',
                        'South Asia', 'Sub-Saharan', 'small states', 'all income', 'blend',
                        'only', 'total', 'Arab World', 'countries', 'Union', 'lending',
                        'Least', 'developing', 'emerging']
    def is_country(name):
        for kw in exclude_keywords:
            if kw.lower() in name.lower():
                return False
        return True

    countries = {}
    for pt in data:
        c = pt['countryName']
        if is_country(c) and pt['value'] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][pt['year']] = pt['value']

    print(f"Individual countries: {len(countries)}")
    return countries, is_country


@app.cell
def _(countries, json):
    slope_data = []
    for c, years in countries.items():
        year_a = None
        for y in range(2000, 1994, -1):
            if y in years:
                year_a = y
                break
        year_b = None
        for y in range(2024, 2017, -1):
            if y in years:
                year_b = y
                break
        if year_a and year_b:
            slope_data.append({"n": c, "a": round(years[year_a], 1), "b": round(years[year_b], 1)})

    mixed = [x for x in slope_data if x['a'] < 90 and x['b'] > 40]
    mixed.sort(key=lambda x: -(x['b'] - x['a']))
    selected = mixed[:25]

    # Shorten long names for display
    name_map = {"Congo, Dem. Rep.": "Congo, Dem. Rep.", "Gambia, The": "Gambia",
                "Dominican Republic": "Dom. Republic", "Egypt, Arab Rep.": "Egypt",
                "Iran, Islamic Rep.": "Iran"}
    for item in selected:
        item['n'] = name_map.get(item['n'], item['n'])

    print(f"Selected {len(selected)} countries for slope chart")
    for x in selected:
        print(f"  {x['n']}: {x['a']} -> {x['b']} (+{x['b']-x['a']:.1f}pp)")
    print(json.dumps(selected, separators=(',', ':')))
    return (selected, slope_data)


if __name__ == "__main__":
    app.run()
