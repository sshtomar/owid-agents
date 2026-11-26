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
        # Learning-Adjusted Years of School -- Methodology

        Slope chart comparing quality-adjusted education years (2010 vs 2020)
        across 16 countries from Singapore to Chad.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--HD-HCI-LAYS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    pts2010 = {p["countryName"]: round(p["value"], 2) for p in data if p["year"] == 2010 and p["value"] is not None}
    pts2020 = {p["countryName"]: round(p["value"], 2) for p in data if p["year"] == 2020 and p["value"] is not None}
    picks = [
        "Singapore", "Finland", "Japan", "United Kingdom", "Poland",
        "Australia", "Germany", "Chile", "Turkey", "Mexico",
        "Brazil", "Indonesia", "South Africa", "Madagascar", "Uganda", "Chad",
    ]
    result = []
    for p in picks:
        a = pts2010.get(p)
        b = pts2020.get(p)
        if a and b:
            result.append({"n": p, "a": a, "b": b})
    result.sort(key=lambda x: -x["b"])
    print(f"Countries: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['a']} -> {r['b']}")
    return picks, pts2010, pts2020, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — comparing two time points across many countries
        - **Country selection**: Diverse income levels from Singapore (top) to Chad (bottom)
        - **Time range**: 2010 vs 2020, the two available years for this metric
        - **Color**: Green for high 2020 scores, amber/red for low scores
        - **Highlights**: 10x gap between Singapore (12.8) and Chad (2.8); South Africa declining
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
