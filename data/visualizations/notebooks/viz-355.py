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
        # International Tourism Arrivals: COVID-19 Collapse — Methodology

        Slope chart showing international tourist arrivals (millions) for top destinations in 2019 vs 2020. Visualises the scale of collapse caused by pandemic travel restrictions.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    rows_2019 = {r["countryName"]: r["value"] for r in data if r["year"] == 2019 and r["value"] is not None}
    rows_2020 = {r["countryName"]: r["value"] for r in data if r["year"] == 2020 and r["value"] is not None}
    both = {n: (v, rows_2020[n]) for n, v in rows_2019.items() if n in rows_2020}
    top = sorted(both.items(), key=lambda x: -x[1][0])[:15]

    print("Top destinations by 2019 arrivals:")
    for n, (a, b) in top:
        pct = round((b - a) / a * 100)
        print(f"  {n}: {a/1e6:.1f}M -> {b/1e6:.1f}M ({pct:+d}%)")
    return both, rows_2019, rows_2020, top


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — directly shows before/after comparison for each country
        - **Country selection**: Top 12 destinations by 2019 arrivals with both years available
        - **Color encoding**: Magnitude of percentage decline (darker red = larger drop)
        - **Highlights**: Hong Kong −94%, Japan −87%, China −81% vs France −46%
        """
    )
    return


@app.cell
def _(json, top):
    labels = {"Hong Kong SAR, China": "Hong Kong", "Korea, Rep.": "South Korea"}
    chart_data = []
    for n, (a, b) in top[:12]:
        pct = round((a - b) / a * 100)
        chart_data.append({"n": labels.get(n, n), "a": round(a / 1e6, 2), "b": round(b / 1e6, 2)})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
