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
        # Political Regime Stacked Area — Methodology

        Stacked area chart showing the count of countries by regime type
        (V-Dem classification) from 1972 to 2025 (viz-514).

        ## Regime Codes
        - 0: Closed Autocracy
        - 1: Electoral Autocracy
        - 2: Electoral Democracy
        - 3: Liberal Democracy
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "owid--1210053.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(json, data):
    from collections import defaultdict
    by_year = defaultdict(lambda: {0: 0, 1: 0, 2: 0, 3: 0})
    for pt in data:
        if pt["value"] is not None:
            v = int(pt["value"])
            if v in [0, 1, 2, 3] and pt["year"] >= 1972:
                by_year[pt["year"]][v] += 1

    years = sorted(by_year.keys())
    chart_data = [
        {"y": y, "c": by_year[y][0], "ea": by_year[y][1], "ed": by_year[y][2], "ld": by_year[y][3]}
        for y in years
    ]

    print(f"Years: {years[0]}-{years[-1]}")
    for row in chart_data[::10]:
        print(f"  {row['y']}: closed={row['c']} el_auto={row['ea']} el_demo={row['ed']} liberal={row['ld']}")

    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
