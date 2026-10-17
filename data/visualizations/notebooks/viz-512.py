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
        # Sanitation Progress Slope Chart — Methodology

        Documents the data pipeline behind viz-512.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WSH_SANITATION_SAFELY_MANAGED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    skip = {'AFR', 'EMR', 'EUR', 'WPR', 'SEAR', 'AMR', 'GLOBAL'}
    real = [x for x in data if x['value'] is not None and x['country'] not in skip]
    by_c = defaultdict(dict)
    for x in real:
        by_c[x['country']][x['year']] = round(x['value'], 1)
    # Find countries with both early (<=2003) and late (>=2019) data
    pairs = []
    for code, vals in by_c.items():
        early = [y for y in vals if y <= 2003]
        late = [y for y in vals if y >= 2019]
        if early and late:
            pairs.append({
                'code': code,
                'a_year': max(early),
                'a': vals[max(early)],
                'b_year': max(late),
                'b': vals[max(late)]
            })
    pairs.sort(key=lambda x: x['b'] - x['a'])
    print(f"Countries with early+late data: {len(pairs)}")
    for p in pairs:
        print(f"  {p['code']}: {p['a_year']}={p['a']}% -> {p['b_year']}={p['b']}% ({p['b']-p['a']:+.0f}pp)")
    return by_c, pairs, real, skip


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — best for showing change between two time points
        - **Country selection**: 19 countries with early (~2001) and late (~2022) data; mix of big gainers, small gainers, and decliners
        - **Color encoding**: Green spectrum for improvement, red spectrum for decline — magnitude-based
        - **Highlights**: India +59pp, Mexico +47pp; Gambia -34pp, Guyana -26pp
        """
    )
    return


if __name__ == "__main__":
    app.run()
