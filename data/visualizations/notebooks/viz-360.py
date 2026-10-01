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
        # Age Dependency Ratio, 1960-2024 -- Methodology

        Trend lines showing the age dependency ratio (proportion of dependents —
        young + old — relative to working-age population). Diverging paths reveal
        aging societies in East Asia and Europe, and still-high dependency in
        Sub-Saharan Africa.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {'Japan', 'Germany', 'Italy', 'South Korea', 'China',
              'India', 'Bangladesh', 'Ethiopia', 'Kenya'}

    cdata = {}
    for row in data:
        if row['countryName'] not in target or row['value'] is None:
            continue
        c = row['countryName']
        if c not in cdata:
            cdata[c] = {}
        cdata[c][row['year']] = round(row['value'], 1)

    # Build series with every-4-year sampling 1960-2024
    result = []
    for c in sorted(cdata.keys()):
        pts = []
        for y in range(1960, 2025, 4):
            if y in cdata[c]:
                pts.append(round(cdata[c][y], 1))
            elif pts:
                pts.append(pts[-1])
            else:
                pts.append(None)
        while pts and pts[-1] is None:
            pts.pop()
        result.append({'n': c, 's': pts, 'y0': 1960, 'step': 4})

    result.sort(key=lambda x: x['s'][-1], reverse=True)
    print(f"Series: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['s'][0]} -> {r['s'][-1]}")
    return result, cdata, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (1960-2024, every 4 years) to show long-run
          demographic transition
        - **Story**: Japan rose from 55 in 1960 to 70 in 2024 as the population
          aged. Kenya and Ethiopia remain very high (~66-73) driven by youth.
          China collapsed then rebounded as one-child generation ages.
          India, Bangladesh converging toward lower dependency.
        - **Color**: Warm for high dependency, cool for low
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
