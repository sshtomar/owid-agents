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
        # Fossil Fuel Energy Consumption Shift — Methodology

        Slope chart comparing fossil fuel share of total energy consumption
        in 1990 vs 2015 for 25 countries across income levels and regions.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-COMM-FO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {
        'Japan', 'Bangladesh', 'Ghana', 'Australia', 'China', 'Germany',
        'Denmark', 'France', 'Italy', 'India', 'Brazil', 'Colombia',
        'Bulgaria', 'Croatia', 'Argentina', 'Ecuador', 'Finland',
        'Indonesia', 'Hungary', 'Korea, Rep.', 'Austria', 'Estonia',
        'Congo, Dem. Rep.', 'Gabon', 'Kenya'
    }
    by_country = {}
    for x in data:
        if x['countryName'] in target and x['value'] is not None and x['value'] > 0 and x['year'] in [1990, 2015]:
            if x['countryName'] not in by_country:
                by_country[x['countryName']] = {}
            by_country[x['countryName']][x['year']] = x['value']
    both = [(c, round(v[1990], 1), round(v[2015], 1)) for c, v in by_country.items() if 1990 in v and 2015 in v]
    both.sort(key=lambda x: x[1] - x[2], reverse=True)
    print(f"Countries: {[c for c, a, b in both]}")
    return both, by_country, target


@app.cell
def _(both, json):
    chart_data = [{"n": c, "a": a, "b": b} for c, a, b in both]
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
