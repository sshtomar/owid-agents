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
        # Youth Population Share (Ages 0-14), 1960-2024 -- Methodology

        Trend lines showing the share of population aged 0-14 for 11 countries
        over six decades. Reveals diverging demographic paths: Sub-Saharan Africa
        with a persistent youth bulge vs. East Asia and Europe aging rapidly.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-0014-TO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected_codes = {'TD', 'KE', 'ET', 'IN', 'BD', 'BR', 'CN', 'DE', 'JP', 'KR', 'IT'}
    name_map = {
        'TD': 'Chad', 'KE': 'Kenya', 'ET': 'Ethiopia', 'IN': 'India',
        'BD': 'Bangladesh', 'BR': 'Brazil', 'CN': 'China',
        'DE': 'Germany', 'JP': 'Japan', 'KR': 'S. Korea', 'IT': 'Italy'
    }
    order = ['TD', 'KE', 'ET', 'IN', 'BD', 'BR', 'CN', 'DE', 'JP', 'KR', 'IT']

    by_country = {}
    for pt in data:
        c = pt['country']
        if c not in selected_codes or pt['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][pt['year']] = pt['value']

    y0, yEnd = 1960, 2024
    chart_data = []
    for c in order:
        if c not in by_country:
            continue
        vals = by_country[c]
        s = [round(vals[y], 1) if y in vals else None for y in range(y0, yEnd + 1)]
        chart_data.append({'n': name_map[c], 'y0': y0, 's': s})
        first = vals.get(1960, 0)
        last = vals.get(2024) or vals.get(2023)
        print(f"{name_map[c]}: 1960={first:.1f}%, 2024={last:.1f}%")
    return chart_data, by_country, name_map, order, selected_codes, y0, yEnd


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (1960-2024, annual)
        - **Country selection**: Three Sub-Saharan Africa countries, four Asia, four Europe/East Asia
        - **Color**: Warm tones for high youth share (Africa), cool for low share (Europe/East Asia)
        - **Story**: Chad went from 41% to 46% youth share — a youth bulge that grew.
          S. Korea dropped from 41% to 11% in just 60 years.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
