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
        # Malaria Mortality Trend Lines — Methodology

        Documents the data pipeline behind viz-513.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--MALARIA_EST_MORTALITY.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    real = [x for x in data if x['value'] is not None and len(x['country']) == 3]
    by_c = defaultdict(dict)
    for x in real:
        by_c[x['country']][x['year']] = round(x['value'], 1)
    # Select high-burden countries
    select = ['BFA', 'COD', 'NGA', 'UGA', 'BDI', 'TZA', 'MLI', 'LBR']
    for code in select:
        if code in by_c:
            vals = sorted(by_c[code].items())
            print(f"  {code}: {vals[0]} -> {vals[-1]}, {len(vals)} data points")
    return by_c, real, select


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows evolution over a 25-year span for multiple countries
        - **Country selection**: 8 highest-burden African countries with multi-year data
        - **Color encoding**: Warm-to-cool by current burden; red for still-high burden, green for most improved
        - **Highlights**: Burkina Faso 374→70 per 100k (−81%); Uganda 175→37 (−79%); Nigeria still at 81 (−55%)
        - **Reference**: Max y-axis at 400 to show full magnitude of Burkina Faso's historical burden
        """
    )
    return


if __name__ == "__main__":
    app.run()
