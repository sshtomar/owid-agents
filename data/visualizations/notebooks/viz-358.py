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
        # Primary School Completion Rate: ~2000 vs. ~2022 — Methodology

        This notebook documents the data pipeline behind viz-358.
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
    from collections import defaultdict
    exclude_words = ['World', 'income', 'countries', 'IDA', 'IBRD', 'dividend', 'HIPC',
                     'East Asia', 'South Asia', 'Sub-Saharan', 'Latin America', 'Middle East',
                     'North America', 'European Union', 'Euro area', 'Arab World',
                     'Caribbean', 'Pacific island', 'Small states', 'Fragile', 'Heavily indebted']

    by_country = defaultdict(dict)
    for row in data:
        name = row['countryName']
        if row['value'] is not None and not any(w.lower() in name.lower() for w in exclude_words):
            by_country[name][row['year']] = row['value']

    selected = {
        "Cote d'Ivoire": "Côte d'Ivoire", "Cambodia": "Cambodia",
        "Congo, Dem. Rep.": "DR Congo", "Ghana": "Ghana", "Bhutan": "Bhutan",
        "Ethiopia": "Ethiopia", "Burkina Faso": "Burkina Faso", "Guinea": "Guinea",
        "India": "India", "Guatemala": "Guatemala", "Dominican Republic": "Dominican Rep.",
        "Jordan": "Jordan", "Indonesia": "Indonesia", "Colombia": "Colombia",
        "Argentina": "Argentina", "Cuba": "Cuba", "Honduras": "Honduras",
        "Germany": "Germany",
    }

    chart_data = []
    for orig, label in selected.items():
        ydata = by_country.get(orig, {})
        before_years = [y for y in range(1998, 2004) if y in ydata and ydata[y] is not None]
        after_years = [y for y in range(2024, 2018, -1) if y in ydata and ydata[y] is not None]
        if before_years and after_years:
            a_year = sorted(before_years)[len(before_years)//2]
            b_year = after_years[0]
            a, b = ydata[a_year], ydata[b_year]
            if a is not None and b is not None and a <= 112 and b <= 112:
                chart_data.append({'n': label, 'a': round(a, 1), 'b': round(b, 1)})

    print(f"Countries: {len(chart_data)}")
    changes = [(x['n'], round(x['b'] - x['a'], 1)) for x in chart_data]
    print("Changes:", sorted(changes, key=lambda x: -x[1]))
    return chart_data, by_country, selected, exclude_words, changes, defaultdict


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — comparing two time points highlights scale of change
        - **Country selection**: 18 countries covering large improvers (SSA, SE Asia), mid-range, and already high performers
        - **Time range**: ~2000 baseline vs. most recent available (typically 2022–2024)
        - **Highlights**: Côte d'Ivoire and Cambodia nearly doubled completion rates; Ethiopia still below 55%
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
