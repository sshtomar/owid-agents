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
        # Primary School Enrollment Surge — Methodology

        Documents the data pipeline behind viz-514.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-ENRR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_keywords = ['World', 'Africa', 'Asia', 'Europe', 'OECD', 'income', 'dividend', 'Arab',
                    'Caribbean', 'Pacific', 'Latin', 'Sub-Saharan', 'Middle East', 'North America',
                    'Fragile', 'IDA', 'IBRD', 'Heavily', 'Least', 'Small', 'states', 'South Asia',
                    'FCV', 'Conflict', 'blend', 'region', 'MENA']
    by_country = {}
    for row in data:
        c = row['countryName']
        if any(kw.lower() in c.lower() for kw in agg_keywords):
            continue
        if row['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][row['year']] = row['value']
    return agg_keywords, by_country


@app.cell
def _(by_country):
    selected = ['Afghanistan', 'Burkina Faso', 'Ethiopia', 'Guinea', 'Chad',
                'Burundi', 'Congo, Dem. Rep.', 'Benin', 'Ghana', 'Cameroon',
                'Kenya', 'India', 'Bangladesh']
    result = []
    for c in selected:
        if c not in by_country:
            continue
        years = by_country[c]
        pts = [{'y': y, 'v': round(years[y], 1)} for y in range(2000, 2023) if y in years]
        if len(pts) >= 5:
            display = c.replace('Congo, Dem. Rep.', 'DR Congo')
            result.append({'n': display, 'pts': pts,
                          'first': pts[0]['v'], 'fy': pts[0]['y'],
                          'last': pts[-1]['v'], 'ly': pts[-1]['y']})
    result.sort(key=lambda x: x['first'])
    print(f"Countries: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['first']:.1f}% ({r['fy']}) -> {r['last']:.1f}% ({r['ly']}) - {len(r['pts'])} pts")
    return result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — shows each country's trajectory as a small multiple
        - **Sort**: By enrollment in 2000 (lowest first) to show which started furthest behind
        - **Story**: Afghanistan, Burkina Faso, Ethiopia: all under 60% in 2000, now above 80-100%
        - **Note**: Values >100% are valid for gross enrollment (older students re-entering)
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
