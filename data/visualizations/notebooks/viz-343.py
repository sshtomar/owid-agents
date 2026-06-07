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
        # Who Registers Their Newborns? — Methodology

        Horizontal bar chart showing birth registration completeness (% of children under 5)
        circa 2014. Data from the World Bank, which aggregates UNICEF MICS and DHS surveys.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-REG-BRTH-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_kw = ['IDA', 'IBRD', 'Sub-Saharan', 'Least developed', 'Heavily indebted', 'Low income', 'Lower middle',
                  'Africa Eastern', 'Africa Western', 'dividend', 'Fragile', 'World', 'Upper middle',
                  'East Asia', 'South Asia', 'Latin America', 'Middle East', 'Europe', 'Central Asia',
                  'Arab World', 'Caribbean', 'Pacific', 'North America', 'OECD', 'Euro area',
                  'demographic', 'developing', 'small states', 'High income', 'Post-demographic',
                  'Central Europe', 'European Union']
    rows_2014 = [r for r in data if r['value'] is not None and r['year'] == 2014
                 and r['country'] and len(r['country']) == 2
                 and not any(kw.lower() in r['countryName'].lower() for kw in exclude_kw)]
    rows_2014.sort(key=lambda r: r['value'])
    chart_data = [{'n': r['countryName'].replace('Egypt, Arab Rep.', 'Egypt'), 'v': round(r['value'], 1)} for r in rows_2014]
    print(f"Countries in 2014: {len(chart_data)}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar — easy to read country names and compare percentages
        - **Year**: 2014 has the best country coverage (32 actual countries)
        - **Color**: Diverging ramp from deep red (<25%) to green (100%)
        - **Key story**: The gulf between sub-Saharan Africa/South Asia and Europe is stark
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
