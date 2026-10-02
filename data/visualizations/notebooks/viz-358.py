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
        # Terrestrial Protected Areas 2013 vs 2024 — Methodology

        Slope chart comparing protected land area percentage between 2013 and 2024
        for 20 countries. Shows conservation momentum and backsliding.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-LND-PTLD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict
    skip_patterns = ['Eastern and Southern','Western and Central','Arab World','Caribbean',
        'Central Europe','Early-demographic','East Asia','Europe &','High income','Latin America',
        'Low &','Low income','Middle income','North America','OECD','South Asia','Sub-Saharan',
        'World','IDA','IBRD','income','Pacific','Africa Eastern','Africa Western','dividend',
        'small states','Baltics','emerging','developing','classification']
    exclude = {'Guam','Gibraltar','Andorra','Aruba','Bermuda','Liechtenstein','Monaco',
               'Least developed countries: UN classification','Greenland','Faroe Islands'}
    def is_region(name):
        return any(p.lower() in name.lower() for p in skip_patterns) or name in exclude
    filtered = [r for r in data if r['value'] is not None and not is_region(r['countryName'])]
    by_country = defaultdict(dict)
    for r in filtered:
        by_country[r['countryName']][r['year']] = r['value']
    both = [(cn, vals) for cn, vals in by_country.items() if 2013 in vals and 2024 in vals]
    both.sort(key=lambda x: x[1][2024] - x[1][2013], reverse=True)
    print(f"Countries with 2013 and 2024: {len(both)}")
    return both, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — 2-point comparison (2013 vs 2024)
        - **Country selection**: 10 biggest gainers + 5 decliners + 5 mid-range
        - **Color**: Warm orange = big gain, cool green = small change, terra = decline
        - **Story**: Bhutan, Croatia, Japan dramatically expanded; Eritrea, Haiti collapsed
        """
    )
    return


@app.cell
def _(both, json):
    gainers = both[:10]
    decliners = [(cn, v) for cn, v in both if v[2024] - v[2013] < -4][:5]
    mid = both[10:20:2]
    selected_set = set(cn for cn, _ in gainers + decliners + mid)
    selected = [(cn, vals) for cn, vals in both if cn in selected_set]
    selected.sort(key=lambda x: x[1][2024], reverse=True)
    chart_data = [{"n": cn, "a": round(vals[2013],1), "b": round(vals[2024],1)} for cn, vals in selected[:25]]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
