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
        # Age Dependency Ratio, 1990-2024 — Methodology

        This notebook documents the data pipeline behind viz-357.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1990 and d["year"] <= 2024 and d["year"] % 2 == 0]
    countries = ["Japan", "Germany", "France", "China", "Brazil", "India", "Bangladesh", "Ethiopia"]
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
        print(f"{c}: {vals[0]['value']:.1f} ({vals[0]['year']}) -> {vals[-1]['value']:.1f} ({vals[-1]['year']})")
    return by_country,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows diverging trajectories over 34 years
        - **Country selection**: Japan (extreme aging), Germany/France (moderate aging), China/Brazil (demographic dividend ending), India/Bangladesh (rapid decline), Ethiopia (still very high)
        - **Time range**: 1990-2024 (every 2 years to keep data compact)
        - **Highlights**: Japan's ratio nearly doubled from 43% to 70%; Ethiopia still above 73% despite major decline from peak of 102%
        """
    )
    return


@app.cell
def _(by_country, json):
    chart_data = []
    for c in ["Japan", "Germany", "France", "China", "Brazil", "India", "Bangladesh", "Ethiopia"]:
        pts = sorted(by_country.get(c, []), key=lambda x: x["year"])
        chart_data.append({"n": c, "pts": [{"y": p["year"], "v": round(p["value"], 1)} for p in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
