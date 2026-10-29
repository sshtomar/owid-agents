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
        # Income Inequality — Top 20% Share — Methodology

        Documents the data pipeline behind viz-515.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-05TH-20.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_country = {}
    for row in data:
        c = row['countryName']
        if row['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][row['year']] = row['value']
    print(f"Countries loaded: {len(by_country)}")
    return (by_country,)


@app.cell
def _(by_country):
    selected = ['Brazil', 'Colombia', 'Ecuador', 'Honduras', 'Argentina', 'Chile', 'Costa Rica',
                'Germany', 'France', 'Finland', 'Belgium', 'Czechia']
    result = []
    for c in selected:
        if c not in by_country:
            continue
        years = by_country[c]
        pts = sorted([{'y': y, 'v': round(v, 1)} for y, v in years.items() if 1990 <= y <= 2024], key=lambda x: x['y'])
        if len(pts) >= 5:
            result.append({'n': c, 'pts': pts, 'last': pts[-1]['v'], 'ly': pts[-1]['y']})

    # Sort by latest value (most unequal first)
    result.sort(key=lambda x: -x['last'])
    print(f"Countries: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['pts'][0]['v']}% ({r['pts'][0]['y']}) -> {r['last']}% ({r['ly']}) - {len(r['pts'])} pts")
    return result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — multiple time series to show evolution of inequality since 1990
        - **Grouping**: Latin American countries (50-65%) vs European countries (32-41%)
        - **Color**: Warm colors for Latin America (high inequality), cool/green for Europe
        - **Story**: Latin America has gradually reduced inequality but the gap with Europe remains enormous
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
