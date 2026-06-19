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
        # Primary School Completion Rate — Methodology

        This notebook documents the pipeline for the slope chart showing
        primary school completion improvements across 20 countries over multiple decades.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    pts = [p for p in data if p['value'] is not None]
    by_country = defaultdict(dict)
    for p in pts:
        by_country[p['countryName']][p['year']] = p['value']

    exclude = ['East ', 'West ', 'World', ' income', 'OECD', 'Asia', 'Africa', 'Europe',
               'America', 'Pacific', 'Arab', 'Caribbean', 'IDA', 'IBRD', 'fragile',
               'Fragile', 'Heavily', 'HIPC', 'small', 'Sub-Saharan', 'Latin',
               'Developing', 'dividend', 'North ', 'Middle East', 'classification', 'Least']

    result = []
    for c, vals in by_country.items():
        if any(t in c for t in exclude):
            continue
        years = sorted(vals.keys())
        if not years or (years[-1] - years[0]) < 5:
            continue
        yr_start, yr_end = years[0], years[-1]
        va, vb = round(vals[yr_start], 1), round(vals[yr_end], 1)
        result.append({'n': c, 'a': va, 'ay': yr_start, 'b': vb, 'by': yr_end, 'chg': vb-va})

    result.sort(key=lambda x: -x['chg'])

    selected = result[:18] + [r for r in result if r['chg'] < 0][:2]
    selected.sort(key=lambda x: -x['chg'])
    chart_data = [{'n': r['n'], 'a': r['a'], 'b': r['b']} for r in selected[:20]]

    print(f"Countries: {len(chart_data)}")
    for r in selected[:20]:
        print(f"  {r['n']}: {r['a']}% ({r['ay']}) -> {r['b']}% ({r['by']}) chg={r['chg']:+.1f}")
    return chart_data, by_country, pts, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — earliest vs latest available year shows the full
          magnitude of change without requiring regular annual data.
        - **Country selection**: 20 countries with largest absolute gains, spanning Africa, Asia,
          and Latin America; captures both fast gainers (Cabo Verde, Bhutan) and slower ones (Burundi).
        - **Story**: Cabo Verde improved from 10% to 99% in ~50 years; most low-income countries
          roughly doubled their completion rates. A few (Burkina Faso, Burundi, Ethiopia)
          remain below 55% despite substantial progress.
        - **Color encoding**: Gain magnitude — >70pp (orange-red), 50-70pp (amber), 30-50pp (yellow), <30pp (green).
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
