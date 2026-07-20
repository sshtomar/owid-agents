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
        # Natural Gas Electricity Share, 1990–2024 — Methodology

        Trend lines showing the share of electricity produced from natural gas
        for 10 countries. Documents data selection and design rationale.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NGAS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    targets = {
        "Israel", "Argentina", "Italy", "Japan", "Greece",
        "World", "Germany", "Australia", "France", "Brazil"
    }
    by_country = defaultdict(list)
    for row in data:
        if row["countryName"] in targets and row["value"] is not None:
            by_country[row["countryName"]].append({"y": row["year"], "v": round(row["value"], 1)})
    for c in targets:
        if c in by_country:
            pts = sorted(by_country[c], key=lambda x: x["y"])
            print(f"{c}: {pts[0]['y']}–{pts[-1]['y']}, {pts[0]['v']}% → {pts[-1]['v']}%")
    return by_country, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows each country's trajectory 1990–2024
        - **Country selection**: Chosen for interesting stories: Israel (domestic gas discovery),
          Japan (post-Fukushima nuclear shutdown), Argentina/Italy (gas-heavy grids),
          Germany/France/Brazil (low or declining gas share)
        - **Color**: Warm-to-cool by 2024 gas share — orange for high dependency, green/blue for low
        - **Highlights**: Israel went from near-0% to 70% after Tamar/Leviathan gas fields opened;
          Japan spiked from 28% to 39% in 2011 after Fukushima shutdowns
        """
    )
    return


@app.cell
def _(json, by_country):
    chart_data = [
        {"n": c, "pts": sorted(by_country[c], key=lambda x: x["y"])}
        for c in ["Israel","Argentina","Italy","Japan","Greece","World","Germany","Australia","France","Brazil"]
        if c in by_country
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
