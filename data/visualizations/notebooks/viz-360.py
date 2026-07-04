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
        # Child Wasting (Acute Undernutrition) -- Methodology

        Horizontal bar chart of child wasting prevalence -- the share of children
        under 5 with low weight-for-height (acute malnutrition). Distinct from
        stunting (chronic) which is already in the catalog. Most recent year per
        country from 2010 onwards.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-WAST-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    skip_kw = ('Africa', 'East', 'Europe', 'Latin', 'Middle', 'North', 'South', 'Sub', 'World', 'High', 'Low', 'Lower', 'Upper', 'Least', 'Fragile', 'Small', 'IBRD', 'IDA', 'OECD', 'Arab', 'Central', 'Pacific', 'Caribbean', 'Heavily', 'income', 'dividend', 'region', 'members', 'countries', 'states', 'Eurasia', 'Asia', 'America', 'Euro', 'island', 'Island')
    by_country = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is not None and not any(k.lower() in c.lower() for k in skip_kw):
            if c not in by_country or y > by_country[c][1]:
                by_country[c] = (v, y)
    recent = [(c, v, y) for c, (v, y) in by_country.items() if y >= 2010]
    recent.sort(key=lambda x: x[1], reverse=True)
    chart_data = recent[:40]
    print(f"Countries with 2010+ data: {len(recent)}, showing top 40")
    print(f"India: {[(c,v,y) for c,v,y in chart_data if c=='India']}")
    return by_country, chart_data, recent


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart -- compare 40 countries by wasting rate
        - **Country selection**: Top 40 by most recent wasting rate (2010+)
        - **WHO emergency threshold**: 15% -- only India exceeds this
        - **Story**: South Asia (India, Bangladesh) and Djibouti are outliers; most of SSA is 5-10%
        - **Contrast with stunting**: India has both the highest wasting AND very high stunting
        """
    )
    return


@app.cell
def _(json, chart_data):
    final = [{"n": c, "v": round(v, 1), "y": y} for c, v, y in chart_data]
    print(json.dumps(final, separators=(",", ":")))
    return (final,)


if __name__ == "__main__":
    app.run()
