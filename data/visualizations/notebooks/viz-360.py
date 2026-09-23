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
        # Marine Protected Areas — Methodology

        Share of territorial waters designated as marine protected areas (%).
        This slope chart compares 2015 vs 2024 for the top 20 countries to show
        the ocean conservation surge over the past decade.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-MRN-PTMR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGG_NAMES = ['Africa','Asia','Europe','America','Arab','Caribbean','OECD','Upper',
                 'Lower','Middle','High','Low','World','Small','East','West','South',
                 'North','Sub-','Pacific','income','dividend','states','countries',
                 'economies','union','Central','Fragile','Heavily','Least','Blend',
                 'Euro','Developing','IDA','IBRD','total']
    code_name = {p['country']: p['countryName'] for p in data if p['value'] is not None}
    agg_codes = {code for code, name in code_name.items() if any(kw in name for kw in AGG_NAMES)}
    country_pts = [p for p in data if p['value'] is not None and p['country'] not in agg_codes]
    print(f"Countries: {len(set(p['country'] for p in country_pts))}")
    return AGG_NAMES, agg_codes, code_name, country_pts


@app.cell
def _(code_name, country_pts, json):
    y2013 = {p['country']: p['value'] for p in country_pts if p['year'] == 2013}
    y2024 = {p['country']: p['value'] for p in country_pts if p['year'] == 2024}

    both = {c: (y2013[c], y2024[c]) for c in y2013 if c in y2024 and y2024[c] > 0.5}
    sorted_both = sorted(both.items(), key=lambda x: -x[1][1])

    chart_data = [
        {"n": code_name.get(code, code), "a": round(a, 1), "b": round(b, 1)}
        for code, (a, b) in sorted_both[:20]
    ]
    print(f"Countries in chart: {len(chart_data)}")
    for row in chart_data:
        print(f"  {row['n']}: {row['a']}% -> {row['b']}% (+{row['b']-row['a']:.1f})")
    print(json.dumps(chart_data, separators=(",", ":")))
    return both, chart_data, sorted_both, y2013, y2024


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — best for before/after comparison across many entities
        - **Years**: 2015 (Paris Agreement year) vs 2024 (most recent)
        - **Country selection**: Top 20 by 2024 protection level
        - **Color**: Warm for big increases (Chile, Colombia, Kazakhstan made enormous gains),
          cool for already high or stable values
        - **Highlights**: Kazakhstan: 1% to 52.5%; Colombia: 2% to 41%; Chile: 4% to 41%
        """
    )
    return


if __name__ == "__main__":
    app.run()
