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
        # Population in Low-Elevation Coastal Zones — Methodology

        Horizontal bar chart showing share of population below 5m elevation (2015).
        Source dataset: wb--EN-POP-EL5M-ZS
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-POP-EL5M-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    vals_2015 = {p["countryName"]: p["value"] for p in data if p["year"] == 2015 and p["value"] is not None}
    skip_words = ["income","Africa","Asia","Europe","America","World","OECD","dividend","Arab","states","IDA","IBRD","South","North","East","West","Central","Caribbean","Euro area","European","Latin","Pacific","Middle","island"]
    clean = {k: v for k, v in vals_2015.items() if not any(w in k for w in skip_words) and v > 0}
    top = sorted(clean.items(), key=lambda x: x[1], reverse=True)
    chart_data = [{"n": n, "v": round(v, 2)} for n, v in top[:25]]
    print(f"Countries with 2015 data: {len(clean)}")
    print(f"Top 10:")
    for n, v in top[:10]:
        print(f"  {n}: {v:.2f}%")
    return chart_data, clean, top, vals_2015


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — clear ranking comparison
        - **Year**: 2015 (most recent in this dataset, which runs 1990/2000/2015)
        - **Country selection**: Top 25 individual countries by share, excluding regional aggregates
        - **Color**: By magnitude (red > 50%, orange 20-50%, amber 10-20%, green < 10%)
        - **Highlights**: Guyana has 78% of its population in low-elevation zones; Bangladesh and Indonesia among the most populous at risk
        - **Context**: LECZ populations face compounding risk from sea-level rise and storm surge
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
