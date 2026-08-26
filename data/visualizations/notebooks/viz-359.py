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
        # Primary School Completion Rate by Income Group, 1990-2024 -- Methodology

        Trend lines showing the share of children completing primary school across
        income groups. The gap between high-income and low-income countries has
        barely narrowed in 30 years.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_group = defaultdict(list)
    for row in data:
        if row["value"] is not None and 1990 <= row["year"] <= 2024:
            by_group[row["countryName"]].append((row["year"], row["value"]))

    groups = ["High income", "Upper middle income", "World", "Lower middle income",
              "Sub-Saharan Africa", "Low income"]
    series = {}
    for g in groups:
        pts = sorted(by_group.get(g, []), key=lambda x: x[0])
        if pts:
            series[g] = pts
            print(f"{g}: {pts[0]} -> {pts[-1]}")
    return (by_group, groups, series)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows progression over time for comparison groups
        - **Groups**: Income classification groups + Sub-Saharan Africa for regional context
        - **Time range**: 1990–2024 — three decades of progress
        - **Color**: Diverging green-to-red scale (green = high completion, red = low)
        - **World reference**: dashed line to avoid visual clutter
        - **Highlights**: Low-income rose from 40% to 63% — progress exists but lags badly.
          South Asia (not shown) had a dramatic rise from 73% in 1999 to 94% by 2024.
        """
    )
    return


@app.cell
def _(json, series):
    chart_data = []
    for name, pts in series.items():
        chart_data.append({"n": name, "pts": [{"y": y, "v": round(v, 1)} for y, v in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
