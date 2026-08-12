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
        # Out-of-Pocket Health Spending, 2000 vs 2022 — Methodology

        Documents the data pipeline for viz-360.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-OOPC-CH-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_keywords = ["Eastern","Western","Central","Arab","Caribbean","Euro","Middle","Africa","Sub-Saharan","Latin","South Asia","Pacific","World","OECD","income","IDA","IBRD","dividend","debt","blend","Fragile","Small","Least","heavily","depopulated","Other","region","global","International"]
    by_country = {}
    for p in data:
        if p["value"] is None:
            continue
        c = p["countryName"]
        if any(x.lower() in c.lower() for x in skip_keywords):
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][p["year"]] = p["value"]

    slope_data = []
    for c, yrs in by_country.items():
        a = yrs.get(2000)
        b = yrs.get(2022) or yrs.get(2021) or yrs.get(2020)
        if a is not None and b is not None:
            slope_data.append({"n": c, "a": round(a, 1), "b": round(b, 1)})

    slope_data.sort(key=lambda x: x["b"], reverse=True)
    print(f"Countries with both endpoints: {len(slope_data)}")
    return (slope_data,)


@app.cell
def _(slope_data):
    top_oop = slope_data[:8]
    biggest_improve = sorted([s for s in slope_data if s["a"] > 30], key=lambda x: x["a"] - x["b"], reverse=True)[:6]
    low_oop = [s for s in slope_data if s["b"] < 15][:5]

    selected = {}
    for s in top_oop + biggest_improve + low_oop:
        selected[s["n"]] = s

    result = sorted(selected.values(), key=lambda x: x["b"], reverse=True)
    print(f"Final set: {len(result)} countries")
    return (result,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows which countries improved or worsened financial protection
        - **Country selection**: Highest OOP burden, biggest improvers, and low-OOP benchmarks
        - **Threshold**: 40% is commonly cited as the level where healthcare becomes catastrophic for households
        - **Highlights**: Armenia and Bangladesh worsened to ~80%; Cote d'Ivoire improved dramatically; European countries are in the 10-15% range
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
