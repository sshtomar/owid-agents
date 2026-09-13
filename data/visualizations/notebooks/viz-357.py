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
        # Population Growth Rate Trends — Methodology

        Trend lines for 12 large countries, 1961–2024.
        """
    )
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
    exclude_keywords = ['World', 'Africa', 'Asia', 'Europe', 'America', 'Pacific', 'income',
                        'OECD', 'IBRD', 'IDA', 'Euro area', 'dividend', 'Caribbean',
                        'Central Europe', 'Fragile', 'HIPC', 'Heavily', 'Latin', 'Middle East',
                        'South Asia', 'Sub-Saharan', 'small states', 'all income', 'blend',
                        'only', 'total', 'Arab World', 'countries', 'Union', 'lending',
                        'Least', 'developing', 'emerging', 'States']
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
                countries[c] = []
            countries[c].append((pt['year'], pt['value']))

    selected_names = ['China', 'India', 'Japan', 'Korea, Rep.', 'Germany', 'Nigeria',
                      'Kenya', 'Brazil', 'Iran, Islamic Rep.', 'Indonesia', 'Bangladesh', 'France']
    print(f"Selected {len(selected_names)} countries")
    return countries, is_country, selected_names


@app.cell
def _(countries, json, selected_names):
    chart_data = []
    for c in selected_names:
        if c in countries:
            pts = sorted(countries[c])
            s = [round(v, 2) for y, v in pts]
            display_name = c.replace('Korea, Rep.', 'South Korea').replace('Iran, Islamic Rep.', 'Iran')
            chart_data.append({"n": display_name, "s": s, "y0": pts[0][0], "step": 1})

    print(f"Chart data: {len(chart_data)} series")
    for item in chart_data:
        print(f"  {item['n']}: {item['y0']}-{item['y0']+len(item['s'])-1}, latest={item['s'][-1]}")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
