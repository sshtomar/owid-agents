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
    # International Tourist Arrivals, 2004–2020 — Methodology

    Documents data pipeline and editorial decisions for viz-359.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target_countries = ['France', 'China', 'Italy', 'Germany', 'Croatia', 'Greece', 'Japan', 'Austria', 'India']
    selected_years = list(range(2004, 2021))

    country_data = {}
    for r in data:
        n = r['countryName']
        if n in target_countries and r.get('value') is not None:
            country_data.setdefault(n, {})[r['year']] = round(r['value'] / 1e6, 2)

    result = []
    for c in target_countries:
        pts = country_data.get(c, {})
        if not pts:
            continue
        series = [pts.get(yr) for yr in selected_years]
        while series and series[-1] is None:
            series.pop()
        result.append({'n': c, 's': series, 'y0': 2004, 'step': 1})

    print(f"Series count: {len(result)}")
    return result, target_countries, selected_years, country_data


@app.cell
def _(result):
    for d in result:
        vals = [v for v in d['s'] if v is not None]
        print(f"{d['n']}: peak={max(vals):.1f}M, 2020={vals[-1] if vals else 'N/A'}M")
    return


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Trend lines — captures sustained growth and then abrupt COVID collapse
    - **Country selection**: 9 major tourism destinations representing Europe, East Asia, and South Asia
    - **Time range**: 2004–2020 (France has nulls before 2004; 2020 captures the COVID collapse)
    - **Story**: Global tourism grew steadily for 15 years then collapsed 60–90% in 2020. Japan's rise from 6M to 32M over 15 years (driven by policy changes) makes the 2020 drop especially stark
    - **Annotation**: COVID band highlights the 2020 anomaly
    """)
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
