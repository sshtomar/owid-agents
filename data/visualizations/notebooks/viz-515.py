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
        # Women 80+ Share — Methodology

        Documents the data pipeline behind viz-515.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-80UP-FE-5Y.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_c = defaultdict(dict)
    for x in data:
        if x['value'] is not None:
            by_c[x['countryName']][x['year']] = round(x['value'], 2)
    select = ['Japan', 'Italy', 'Germany', 'France', 'Korea, Rep.', 'Australia', 'China', 'Sub-Saharan Africa']
    years_5y = list(range(1960, 2021, 5))
    for name in select:
        if name in by_c:
            vals = [(y, by_c[name][y]) for y in years_5y if y in by_c[name]]
            print(f"  {name}: {vals[0]} -> {vals[-1]}, {len(vals)} quinquennial points")
    return by_c, select, years_5y


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — reveals the dramatic demographic divergence over 64 years
        - **Country selection**: 8 series representing different aging trajectories (fast: Japan, Italy; moderate: France, Germany; accelerating: Korea; slow: China, Brazil; flat: Sub-Saharan Africa)
        - **Time range**: 1960–2024 (quinquennial data + 2024 endpoint)
        - **Key insight**: Japan at 12.9% women 80+; Sub-Saharan Africa at 0.5% — a 26-fold gap driven by longevity, fertility, and healthcare
        - **Note**: "Sub-Saharan Africa" is the World Bank regional aggregate; data for individual African countries is sparse
        """
    )
    return


if __name__ == "__main__":
    app.run()
