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
        # Tuberculosis Incidence: 2000 vs. 2022 — Methodology

        This notebook documents the data pipeline behind viz-359.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-TBS-INCD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = ["India", "China", "Indonesia", "Bangladesh", "Congo, Dem. Rep.", "Brazil", "Kenya", "Ethiopia", "Cambodia"]
    filtered = [d for d in data if d["value"] is not None and d["countryName"] in countries and d["year"] in [2000, 2022]]
    print(f"After filtering: {len(filtered)} rows")
    return countries, filtered


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for d in filtered:
        by_country[d["countryName"]][d["year"]] = d["value"]
    for c, yrs in sorted(by_country.items()):
        if 2000 in yrs and 2022 in yrs:
            pct = (yrs[2022] - yrs[2000]) / yrs[2000] * 100
            print(f"{c}: {yrs[2000]:.0f} (2000) -> {yrs[2022]:.0f} (2022)  {pct:+.0f}%")
    return by_country,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compare two time points across many countries, colored by magnitude of decline
        - **Country selection**: High-burden countries (WHO top 30 TB list) with complete 2000 and 2022 data
        - **Time range**: 2000 vs 2022 (earliest and most recent full year in dataset)
        - **Highlights**: Ethiopia -70%, Cambodia -68% (fast decliners); Indonesia and Bangladesh essentially flat
        """
    )
    return


@app.cell
def _(by_country, json):
    chart_data = []
    display = {"Congo, Dem. Rep.": "Congo, DR"}
    for c in ["India", "China", "Indonesia", "Bangladesh", "Congo, Dem. Rep.", "Brazil", "Kenya", "Ethiopia", "Cambodia"]:
        yrs = by_country.get(c, {})
        if 2000 in yrs and 2022 in yrs:
            chart_data.append({"n": display.get(c, c), "a": round(yrs[2000], 0), "b": round(yrs[2022], 0)})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, display


if __name__ == "__main__":
    app.run()
