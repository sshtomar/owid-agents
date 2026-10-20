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
        # Anemia in Pregnancy: High-Burden Countries, 2000 vs 2023 -- Methodology

        Slope chart comparing anemia prevalence among pregnant women
        between ~2000 and ~2023 for the 20 highest-burden countries.
        Source: World Bank (SH.PRG.ANEM), derived from WHO/UNICEF estimates.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-PRG-ANEM.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} rows")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict

    exclude = ['Africa', 'Asia', 'Europe', 'World', 'income', 'IBRD', 'IDA',
               'Latin', 'East', 'South', 'North', 'Sub', 'states', 'Central', 'small',
               'Pacific', 'Caribbean', 'fragile', 'HIPC', 'Least', 'OECD', 'Arab',
               'Heavily', 'Island', 'upper', 'lower', 'dividend', 'Conflict', 'Violence']

    by_ctry = defaultdict(dict)
    for r in data:
        nm = r['countryName']
        if r['value'] is not None and not any(x.lower() in nm.lower() for x in exclude):
            by_ctry[nm][r['year']] = r['value']

    slope = []
    for name, yrs in by_ctry.items():
        early = [(y, v) for y, v in yrs.items() if 2000 <= y <= 2003]
        late = [(y, v) for y, v in yrs.items() if 2020 <= y <= 2023]
        if early and late:
            a_yr, a_v = max(early, key=lambda x: x[0])
            b_yr, b_v = max(late, key=lambda x: x[0])
            slope.append({'n': name, 'a': round(a_v, 1), 'b': round(b_v, 1)})

    slope.sort(key=lambda x: -x['b'])
    chart_data = slope[:20]
    print(f"Countries in chart: {len(chart_data)}")
    for s in chart_data:
        print(f"  {s['n']}: {s['a']:.1f} -> {s['b']:.1f}")
    return chart_data, slope, by_ctry, exclude


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — connects each country's value at two time points
        - **Countries**: Top 20 highest-burden in 2023, all with ~2000 data
        - **Time points**: ~2000 (earliest available) and ~2023 (most recent)
        - **Highlights**: West Africa dominates; India shows modest improvement; Burundi worsened
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
