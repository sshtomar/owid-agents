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
        # Exclusive Breastfeeding Rates — Methodology

        This notebook documents the pipeline for the slope chart showing
        breastfeeding rate improvements across 20 countries with the largest absolute gains.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-BFED-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    pts = [p for p in data if p['value'] is not None]
    by_country = defaultdict(list)
    for p in pts:
        by_country[p['countryName']].append((p['year'], p['value']))

    exclude = ['East ', 'West ', 'World', ' income', 'OECD', 'Asia', 'Africa', 'Europe',
               'America', 'Pacific', 'Arab', 'Caribbean', 'IDA', 'IBRD', 'fragile',
               'Fragile', 'Heavily', 'HIPC', 'small states', 'Sub-Saharan', 'Latin',
               'Developing', 'dividend', 'Middle East', 'North ', 'South ', 'Central ']

    result = []
    for c, vals in by_country.items():
        if any(t in c for t in exclude):
            continue
        vals_sorted = sorted(vals)
        if len(vals_sorted) < 2 or (vals_sorted[-1][0] - vals_sorted[0][0]) < 5:
            continue
        earliest = vals_sorted[0]
        latest = vals_sorted[-1]
        result.append({'n': c, 'a': round(earliest[1], 1), 'ay': earliest[0], 'b': round(latest[1], 1), 'by': latest[0], 'chg': latest[1]-earliest[1]})

    result.sort(key=lambda x: -x['chg'])
    chart_data = [{'n': r['n'], 'a': r['a'], 'b': r['b']} for r in result[:20]]

    print(f"Countries: {len(chart_data)}")
    for r in result[:20]:
        print(f"  {r['n']}: {r['a']}% ({r['ay']}) -> {r['b']}% ({r['by']}) +{r['chg']:.1f} pp")
    return chart_data, by_country, pts, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-time-point comparison is the ideal format here
          since data is survey-based, not annual.
        - **Country selection**: 20 countries with largest absolute percentage-point gains.
        - **Story**: Many countries started near 0% in the 1980s-90s; targeted health
          interventions (WHO Baby-Friendly Hospital Initiative, community health workers)
          drove dramatic uptake. Croatia's rise from 24% to 98% in 12 years is remarkable.
        - **Color encoding**: Magnitude of gain (>60pp, 40-60pp, 20-40pp, <20pp).
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
