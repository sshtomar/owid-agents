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
        # Social Protection Coverage Bar Chart — Methodology

        Horizontal bar chart showing social protection coverage (% of population)
        for the top 25 countries with available data.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--per_allsp-cov_pop_tot.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_terms = ['income', 'World', 'OECD', 'IDA', 'IBRD', 'Pacific', 'Arab', 'Caribbean',
                  'states', 'region', 'countries', 'dividend', 'fragile', 'small', 'Africa',
                  'Asia', 'America', 'Middle East', 'South Asia', 'Sub-Saharan', 'North America',
                  'Euro area', 'European Union', 'Europe', 'Latin', 'only']
    countries = {}
    for row in data:
        c = row['countryName']
        if row['value'] is not None and not any(x.lower() in c.lower() for x in skip_terms):
            if c not in countries or row['year'] > countries[c][0]:
                countries[c] = (row['year'], round(row['value'], 1))
    sorted_c = sorted(countries.items(), key=lambda x: -x[1][1])
    print(f"Countries with data: {len(sorted_c)}")
    print("Top 5:")
    for c, (y, v) in sorted_c[:5]:
        print(f"  {c} ({y}): {v}%")
    return countries, sorted_c


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — best for comparing many countries on a single metric
        - **Metric**: % of population covered by at least one social protection or labor program (most recent year available)
        - **Color**: Green-to-red gradient based on coverage level (green = comprehensive, red = sparse)
        - **Notable**: Bolivia leads at 97%; wide variation between similar-income countries highlights policy choices
        """
    )
    return


if __name__ == "__main__":
    app.run()
