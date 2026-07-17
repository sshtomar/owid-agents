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
        # HIV ART Coverage Slope Chart — Methodology

        Slope chart comparing antiretroviral therapy (ART) coverage for people living with HIV,
        2010 vs. 2024, across 17 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-HIV-ARTC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregates = ['Africa', 'Asia', 'America', 'World', 'IDA', 'IBRD', 'OECD', 'Heavily',
                  'Sub-Saharan', 'income', 'dividend', 'Latin', 'Europe', 'Caribbean', 'Least',
                  'classification', 'Pre-']
    c2010 = {p['countryName']: p['value'] for p in data if p['year'] == 2010 and p.get('value') is not None
             and not any(a in p['countryName'] for a in aggregates)}
    c2024 = {p['countryName']: p['value'] for p in data if p['year'] == 2024 and p.get('value') is not None}
    include = [
        'Ireland', 'Botswana', 'Eswatini', 'Burundi', 'Cambodia', 'Ethiopia', 'Cameroon',
        'Kenya', 'Benin', 'Haiti', "Cote d'Ivoire", 'Angola', 'Ghana', 'Indonesia',
        'Congo, Rep.', 'Djibouti', 'Afghanistan'
    ]
    chart_data = [{'n': c, 'a': round(c2010[c], 1), 'b': round(c2024[c], 1)}
                  for c in include if c in c2010 and c in c2024]
    chart_data.sort(key=lambda x: x['b'], reverse=True)
    print(f"Chart data: {len(chart_data)} countries")
    print(f"Range 2024: {min(x['b'] for x in chart_data):.0f}% - {max(x['b'] for x in chart_data):.0f}%")
    return c2010, c2024, chart_data, include


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares two time points for many entities
        - **Year selection**: 2010 vs. 2024 — 2010 marks when ART scale-up was underway globally
        - **Country selection**: Mix of high achievers (Botswana, Eswatini) and laggards (Afghanistan, Djibouti)
        - **Color**: Encodes change magnitude — darker green = larger gain
        - **Highlights**: Sub-Saharan Africa's transformation from near-zero to 80-95% coverage
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
