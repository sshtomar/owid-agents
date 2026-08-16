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
        # Energy Intensity Slope Chart — Methodology

        Documents the data pipeline for viz-358: slope chart comparing energy intensity
        (MJ per $ GDP) across 16 countries, 2000 vs 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-EGY-PRIM-PP-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    c_2000 = {}
    c_2022 = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is None:
            continue
        if y == 2000:
            c_2000[c] = round(v, 2)
        if y == 2022:
            c_2022[c] = round(v, 2)

    both = set(c_2000.keys()) & set(c_2022.keys())
    print(f"Countries with 2000 and 2022 data: {len(both)}")
    by_reduction = sorted(
        [(c, c_2000[c], c_2022[c]) for c in both if c_2000[c] > 0 and c_2022[c] > 0],
        key=lambda x: (x[2] - x[1]) / x[1]
    )
    print("Top reducers:")
    for name, v0, v1 in by_reduction[:8]:
        pct = (v1 - v0) / v0 * 100
        print(f"  {name}: {v0} -> {v1} ({pct:+.0f}%)")
    return both, by_reduction, c_2000, c_2022


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point comparison clearly shows direction and magnitude
        - **Country selection**: Mix of large economies (Germany, France, Japan, Canada) and
          standout performers (Ireland -69%, Azerbaijan -69%, Bulgaria -48%)
        - **Time range**: 2000–2022 (energy intensity data starts at 2000)
        - **Color**: Diverging green/amber/red by improvement percentage
        - **Story**: Almost every country improved, but the range is enormous
        """
    )
    return


@app.cell
def _(json, c_2000, c_2022):
    selected = ['Germany', 'France', 'Japan', 'Australia', 'Canada', 'Ireland',
                'Azerbaijan', 'Bulgaria', 'Estonia', 'Albania', 'Israel', 'Czechia',
                'Finland', 'Brazil', 'Italy', 'Korea, Rep.']
    name_map = {'Korea, Rep.': 'South Korea'}
    chart_data = []
    for c in selected:
        if c in c_2000 and c in c_2022:
            chart_data.append({"n": name_map.get(c, c), "a": c_2000[c], "b": c_2022[c]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, name_map, selected
