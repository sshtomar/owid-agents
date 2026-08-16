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
        # Preprimary Enrollment Trend Lines — Methodology

        Documents the data pipeline for viz-359: regional trend lines for preprimary
        school enrollment, 1970–2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRE-ENRR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    regions = ['World', 'Sub-Saharan Africa', 'South Asia', 'East Asia & Pacific',
               'Europe & Central Asia', 'Latin America & Caribbean']
    result = {}
    for row in data:
        c = row['countryName']
        if c not in regions:
            continue
        y = row['year']
        v = row['value']
        if v is None:
            continue
        if c not in result:
            result[c] = {}
        result[c][y] = round(v, 1)

    for c in regions:
        if c in result:
            pts = sorted(result[c].items())
            print(f"{c}: {pts[0]} -> {pts[-1]}, n={len(pts)}")
    return regions, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the long arc of investment in early childhood ed
        - **Entities**: World regions (not individual countries) to show structural patterns
        - **Time range**: 1970–2020 (full available regional series)
        - **Story**: East Asia surged from 5% to 83% in 47 years. Sub-Saharan Africa at 28%
          remains far behind, with major implications for school readiness and human capital.
        - **World** shown as dashed reference line
        """
    )
    return


@app.cell
def _(json, result):
    chart_data = []
    for c, pts_dict in result.items():
        yrs = sorted(pts_dict.keys())
        chart_data.append({
            "n": c,
            "s": [pts_dict[y] for y in yrs],
            "y0": yrs[0]
        })
    print(json.dumps(chart_data[:2], separators=(",", ":")))
    return (chart_data,)
