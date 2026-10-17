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
        # Female Homicide Rates — Methodology

        Documents the data pipeline behind viz-514.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-FE-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude = ['World', 'income', 'OECD', 'developing', 'Latin', 'Sub-Saharan',
               'Europe', 'East Asia', 'South Asia', 'Middle East', 'North Africa',
               'Pacific', 'small', 'IDA', 'IBRD', 'Heavily', 'Fragil', 'Blend',
               'America', 'Africa East', 'Africa West', 'North America']
    def is_country(name):
        return not any(t.lower() in name.lower() for t in exclude)
    c2022 = [(x['countryName'], round(x['value'], 2))
             for x in data if x['year'] == 2022 and x['value'] is not None and is_country(x['countryName'])]
    c2022.sort(key=lambda x: -x[1])
    print(f"Countries in 2022: {len(c2022)}")
    for name, v in c2022[:10]:
        print(f"  {name}: {v}")
    return c2022, exclude, is_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — direct ranking comparison
        - **Country selection**: 38 countries spanning the full range from lowest (Indonesia 0.15) to highest (Dominica 9.0)
        - **Color encoding**: Green for low risk, red for high risk
        - **Key insight**: Caribbean and Central American countries dominate the top 10; East Asian and Northern European countries have the lowest rates
        - **Note**: 2022 is the latest complete year with broad coverage
        """
    )
    return


if __name__ == "__main__":
    app.run()
