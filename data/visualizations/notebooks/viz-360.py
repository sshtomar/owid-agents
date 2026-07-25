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
        # Manufacturing as % of GDP — Methodology

        Documents the data pipeline behind viz-360.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-MANF-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries_map = {
        "Korea, Rep.": "South Korea",
        "Viet Nam": "Vietnam",
    }
    target = ["China", "Korea, Rep.", "Germany", "Japan", "India", "Indonesia", "Bangladesh", "Brazil"]
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in data:
        if row["countryName"] in target and row["value"] is not None and row["value"] > 0:
            by_country[row["countryName"]].append((row["year"], round(row["value"], 1)))

    chart_data = []
    for name in target:
        label = countries_map.get(name, name)
        pts = sorted(by_country[name])
        if pts:
            chart_data.append({"n": label, "pts": [{"y": y, "v": v} for y, v in pts]})
            print(f"{label}: {pts[0]} -> {pts[-1]}")
    return by_country, chart_data, countries_map, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — captures the structural shift over time
        - **Country selection**: Represents three waves of industrialization
          (Japan/Germany = mature; South Korea/China = second wave; Bangladesh/Indonesia = third wave)
        - **Observation**: China peaked around 31-32% in 2004-2012 and has been declining,
          following the same deindustrialization path as earlier developers.
          Bangladesh is rising rapidly (5% in 1960, 22% in 2024) driven by garments.
          India has remained surprisingly flat at 13-17%, below its potential.
        - **Brazil excluded from long series**: Pre-1985 data is anomalous; using 1985 onward.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
