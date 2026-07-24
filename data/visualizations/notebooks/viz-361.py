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
        # Population Growth Rate, 1980-2024 — Methodology

        This notebook documents the data pipeline behind viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = ["Sub-Saharan Africa", "Ethiopia", "India", "Brazil", "Bangladesh", "China", "Germany", "Japan"]
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1980 and d["year"] % 2 == 0 and d["countryName"] in countries]
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
        print(f"{c}: {vals[0]['value']:.2f}% ({vals[0]['year']}) -> {vals[-1]['value']:.2f}% ({vals[-1]['year']})")
    return by_country,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with zero-line reference — shows convergence toward and crossing of zero growth
        - **Country selection**: Sub-Saharan Africa (still >2.4%), Ethiopia (high with historical spike), India/Brazil/Bangladesh (fast decline), China/Japan (crossing into negative), Germany (flat)
        - **Time range**: 1980-2024 (every 2 years)
        - **Highlights**: Japan (-0.44%) and China (-0.12%) now shrinking; Sub-Saharan Africa remains at 2.44%
        """
    )
    return


@app.cell
def _(by_country, json):
    chart_data = []
    for c in ["Sub-Saharan Africa", "Ethiopia", "India", "Brazil", "Bangladesh", "China", "Germany", "Japan"]:
        pts = sorted(by_country.get(c, []), key=lambda x: x["year"])
        chart_data.append({"n": c, "pts": [{"y": p["year"], "v": round(p["value"], 2)} for p in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
