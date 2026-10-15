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
        # Part-Time Employment Sparkline Grid — Methodology

        Sparkline grid showing part-time employment trends for 22 countries, 2000–2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-PART-ZS.json"
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
                  'Euro area', 'European Union', 'Europe', 'Latin']
    countries = {}
    for row in data:
        c = row['countryName']
        if row['value'] is not None and not any(x.lower() in c.lower() for x in skip_terms):
            if c not in countries:
                countries[c] = {}
            countries[c][row['year']] = round(row['value'], 1)
    good = {c: v for c, v in countries.items() if 2000 in v and 2022 in v}
    print(f"Countries with 2000-2022 data: {len(good)}")
    result = []
    for c, yv in good.items():
        s = [yv.get(y) for y in range(2000, 2023) if y in yv]
        pts = [(y, yv[y]) for y in range(2000, 2023) if y in yv]
        if len(pts) >= 15:
            values = [p[1] for p in pts]
            result.append({'n': c, 'e': values[0], 'l': values[-1], 's': values, 'y0': pts[0][0]})
    result.sort(key=lambda x: -x['l'])
    print(f"Series with 15+ points: {len(result)}")
    all_values = [v for r in result for v in r['s']]
    print(f"Value range: {min(all_values):.1f} - {max(all_values):.1f}%")
    return all_values, good, pts, result, s, values


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — shows many trends at once in a compact grid, sorted by latest value
        - **Country selection**: 22 countries with consistent annual data 2000-2022
        - **Notable**: Austria rose from 24% to 49% (doubled); Denmark fell from 50% to 44%; South Korea nearly tripled
        - **COVID effect**: Visible as spikes/dips around 2020-2021 in many countries
        """
    )
    return


if __name__ == "__main__":
    app.run()
