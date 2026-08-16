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
        # Old-Age Dependency Ratio — Methodology

        Documents the data pipeline for viz-357: trend lines of old-age dependency
        ratio across 8 countries, 1960–2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = ['Japan', 'Korea, Rep.', 'Italy', 'Germany', 'France', 'China', 'Brazil', 'India']
    result = {}
    for row in data:
        c = row['countryName']
        if c not in countries:
            continue
        y = row['year']
        v = row['value']
        if v is None:
            continue
        if c not in result:
            result[c] = {}
        result[c][y] = round(v, 2)

    print(f"Countries found: {list(result.keys())}")
    for c in countries:
        if c in result:
            pts = sorted(result[c].items())
            print(f"  {c}: {pts[0]} -> {pts[-1]}, n={len(pts)}")
    return countries, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — annual data shows gradual acceleration of aging
        - **Country selection**: Japan (extreme outlier), South Korea (recent rapid aging),
          Italy/Germany/France (established European aging), China (1-child policy effects),
          Brazil/India (still relatively young)
        - **Time range**: 1960–2024 (full series since World Bank data begins)
        - **Highlights**: Japan's 5.7x surge is the core story; shows aging is a global
          phenomenon but at very different speeds
        """
    )
    return


@app.cell
def _(json, result):
    name_map = {'Korea, Rep.': 'South Korea'}
    chart_data = []
    for c, pts_dict in result.items():
        yrs = sorted(pts_dict.keys())
        display = name_map.get(c, c)
        chart_data.append({
            "n": display,
            "s": [pts_dict[y] for y in yrs],
            "y0": yrs[0]
        })
    print(json.dumps(chart_data[:2], separators=(",", ":")))
    return chart_data, name_map
