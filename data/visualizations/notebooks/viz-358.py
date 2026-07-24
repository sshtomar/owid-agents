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
        # Patent Applications by Residents, 1990-2021 — Methodology

        This notebook documents the data pipeline behind viz-358.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1990]
    countries = ["China", "Japan", "Korea, Rep.", "Germany", "India"]
    filtered = [d for d in filtered if d["countryName"] in countries]
    print(f"After filtering: {len(filtered)} rows")
    return countries, filtered


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(list)
    for d in filtered:
        by_country[d["countryName"]].append(d)
    for c, pts in sorted(by_country.items()):
        vals = sorted(pts, key=lambda x: x["year"])
        print(f"{c}: {vals[0]['value']:,.0f} ({vals[0]['year']}) -> {vals[-1]['value']:,.0f} ({vals[-1]['year']})")
    return by_country,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows exponential rise of China vs. stagnation of other countries
        - **Country selection**: China (explosive growth), Japan (decline), South Korea (steady growth), Germany (flat), India (emerging)
        - **Time range**: 1990-2021 (all available years)
        - **Highlights**: China went from 5,832 patents in 1990 to 1.4M in 2021, surpassing Japan's peak of ~390K around 2000
        """
    )
    return


@app.cell
def _(by_country, json):
    display_names = {"Korea, Rep.": "South Korea"}
    chart_data = []
    for c in ["China", "Japan", "Korea, Rep.", "Germany", "India"]:
        pts = sorted(by_country.get(c, []), key=lambda x: x["year"])
        chart_data.append({"n": display_names.get(c, c), "pts": [{"y": p["year"], "v": int(p["value"])} for p in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, display_names


if __name__ == "__main__":
    app.run()
