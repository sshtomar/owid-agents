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
        # DPT Immunization Coverage Since 1980 -- Methodology

        Trend lines showing the rise in diphtheria-tetanus-pertussis (DPT) vaccination
        coverage among children 12-23 months from 1980 to 2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IDPT.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    selected = ["World", "Sub-Saharan Africa", "South Asia", "India", "Ethiopia", "China", "Brazil"]
    years = list(range(1980, 2025, 2))

    result = []
    for c in selected:
        if c in by_country:
            vals = by_country[c]
            pts = [{"y": y, "v": round(vals[y], 1)} for y in years if y in vals]
            if pts:
                result.append({"n": c, "pts": pts})

    for r in result:
        pts = r["pts"]
        print(f"{r['n']}: {pts[0]['y']}={pts[0]['v']}% -> {pts[-1]['y']}={pts[-1]['v']}%")
    return by_country, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines over time -- shows the global health progress story
        - **Series**: World average, two low-income regions, plus 4 large countries
        - **Key events**: COVID-19 dip visible in 2020 for all series
        - **Story**: World went from 17% in 1980 to 85% by 2024; Sub-Saharan Africa
          still lags but gained 70 points; South Asia and India now outperform global average
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
