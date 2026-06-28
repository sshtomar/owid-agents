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
        # Coal in the Electricity Mix -- Methodology

        Slope chart comparing each country's coal share of electricity production
        in 1990 versus 2023, revealing which countries phased out coal and which
        expanded it.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-COAL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    selected = {
        'DK': 'Denmark', 'GR': 'Greece', 'IE': 'Ireland', 'DE': 'Germany',
        'IL': 'Israel', 'AU': 'Australia', 'CZ': 'Czechia', 'EE': 'Estonia',
        'HK': 'Hong Kong', 'BW': 'Botswana', 'IN': 'India', 'ID': 'Indonesia',
        'CN': 'China', 'JP': 'Japan', 'KR': 'S. Korea', 'KZ': 'Kazakhstan',
        'BA': 'Bosnia', 'BG': 'Bulgaria', 'SZ': 'Eswatini', 'CL': 'Chile',
    }

    by_country = defaultdict(dict)
    for x in data:
        if x['country'] in selected and x['value'] is not None:
            by_country[x['country']][x['year']] = x['value']

    chart_data = []
    for cc, name in selected.items():
        yrs = by_country[cc]
        a = yrs.get(1990)
        b = yrs.get(2023) or yrs.get(2022)
        if a is not None and b is not None:
            chart_data.append({'n': name, 'a': round(a, 1), 'b': round(b, 1)})

    chart_data.sort(key=lambda x: -x['a'])
    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f})")
    return chart_data, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (two columns: 1990 vs 2023)
        - **Color**: Red for >+10pp increase, green for >-20pp decline, grey for stable
        - **Story**: Europe dramatically cut coal (Denmark 91%->8%, Greece 72%->9%, Ireland 56%->4%)
          while Indonesia surged from 30% to 69%, India from 65% to 74%.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
