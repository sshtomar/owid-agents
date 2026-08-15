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
        # Income Share of Top 10% — Methodology

        Slope chart comparing each country's income share held by the top 10%
        around 2000 vs. around 2020. Reveals how inequality shifted over two decades.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-10TH-10.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]].append((row["year"], row["value"]))

    results = []
    for country, pts in by_country.items():
        before_pts = [(y, v) for y, v in pts if 1997 <= y <= 2003]
        after_pts = [(y, v) for y, v in pts if 2018 <= y <= 2024]
        if before_pts and after_pts:
            b_year, b_val = max(before_pts, key=lambda x: x[0])
            a_year, a_val = max(after_pts, key=lambda x: x[0])
            results.append({"n": country, "a": round(b_val, 1), "b": round(a_val, 1)})

    results.sort(key=lambda x: x["b"], reverse=True)
    chart_data = results[:25]
    chart_data.sort(key=lambda x: x["a"])
    print(f"Countries in chart: {len(chart_data)}")
    print(f"Range (before): {min(x['a'] for x in chart_data):.1f} – {max(x['a'] for x in chart_data):.1f}")
    print(f"Range (after): {min(x['b'] for x in chart_data):.1f} – {max(x['b'] for x in chart_data):.1f}")
    return chart_data, by_country, results


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparison across many countries
        - **Country selection**: Top 25 by most recent income share, covers Latin America,
          Africa, Asia, and Eastern Europe
        - **Time range**: ~2000 vs ~2020 (using nearest available year in each window)
        - **Highlights**: Most Latin American countries show declining top-10% share;
          Bulgaria, Indonesia show increases
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
