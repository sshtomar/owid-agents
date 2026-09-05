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
        # International Tourist Arrivals, 1995-2020 -- Methodology

        Trend line chart showing annual tourist arrivals (millions) for top destination
        countries from 1995 to 2020. The COVID-19 collapse in 2020 is a central story.
        """
    )
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
    from collections import defaultdict

    selected = ['France', 'Italy', 'Germany', 'Greece', 'Japan', 'Korea, Rep.', 'Croatia', 'Austria', 'Hungary', 'Indonesia']

    by_country = defaultdict(dict)
    for p in data:
        if p['countryName'] in selected and p['value'] is not None:
            by_country[p['countryName']][p['year']] = p['value']

    result = []
    for c in selected:
        series = []
        for yr in range(1995, 2021):
            v = by_country[c].get(yr)
            series.append(round(v / 1e6, 2) if v is not None else None)
        display = c.replace('Korea, Rep.', 'South Korea')
        result.append({'n': display, 's': series, 'y0': 1995})

    for r in result:
        vals = [v for v in r['s'] if v is not None]
        print(f"{r['n']}: {min(vals):.1f}M - {max(vals):.1f}M arrivals (2020: {r['s'][-1]}M)")
    return result, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines for multi-country time series comparison
        - **Country selection**: Top 10 by 2019 arrivals that also have 2020 data (COVID collapse)
        - **COVID band**: Highlight 2020 column to emphasize the shock
        - **Story**: France leads globally with ~218M arrivals in 2019, falling to 117M in 2020.
          Asian destinations (Japan, South Korea) saw the steepest drops (-87%, -86%).
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
