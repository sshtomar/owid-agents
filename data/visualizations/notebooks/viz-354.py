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
        # Safely Managed Drinking Water by Income Group -- Methodology

        Trend lines for % of population using safely managed drinking water services,
        by World Bank income group and key regional aggregates, 2000-2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-H2O-SMDW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for p in data:
        if p['value'] is not None:
            by_country[p['countryName']][p['year']] = round(p['value'], 1)

    regions = [
        ('High income', 'High Income'),
        ('Upper middle income', 'Upper Middle Income'),
        ('Latin America & Caribbean', 'Latin America'),
        ('East Asia & Pacific', 'East Asia & Pacific'),
        ('Lower middle income', 'Lower Middle Income'),
        ('South Asia', 'South Asia'),
        ('Low income', 'Low Income'),
        ('Sub-Saharan Africa', 'Sub-Saharan Africa'),
    ]

    chart_data = []
    for orig, display in regions:
        if orig in by_country:
            pts = [(y, v) for y, v in sorted(by_country[orig].items()) if 2000 <= y <= 2024]
            # Use every 2 years to reduce data size
            pts_sub = [p for p in pts if (p[0] - 2000) % 2 == 0]
            chart_data.append({'n': display, 'pts': [{'y': y, 'v': v} for y, v in pts_sub]})

    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        if s['pts']:
            print(f"  {s['n']}: {s['pts'][0]['v']} -> {s['pts'][-1]['v']}")
    return by_country, chart_data, regions


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows 25-year progress trajectory
        - **Groups**: income tiers + South Asia and Sub-Saharan Africa (biggest stories)
        - **Story**: South Asia nearly doubled access (41%->78%); Sub-Saharan Africa
          barely reached 32% despite progress; gap between high-income (96%) and
          low-income (33%) nations has barely narrowed in absolute terms
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
