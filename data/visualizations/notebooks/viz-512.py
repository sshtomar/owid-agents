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
        # Trade in Services (% of GDP) -- Methodology

        Documents the data pipeline for the services economy visualization.
        Shows how different economies have shifted toward services-based trade.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--BG-GSR-NFSV-GD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1995 and d["year"] <= 2023]
    countries = ["Denmark", "Estonia", "Belgium", "Hong Kong SAR, China", "Austria",
                 "Germany", "India", "China", "Greece", "Croatia", "France", "Japan"]
    by_country = {}
    for row in filtered:
        if row["countryName"] in countries:
            by_country.setdefault(row["countryName"], []).append(row)
    for c, pts in by_country.items():
        vals = [p["value"] for p in pts]
        print(f"{c}: {len(pts)} pts, max={max(vals):.1f}%, latest={vals[-1]:.1f}%")
    return by_country, countries, filtered


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows economic structure shift over 1995-2023
        - **Country selection**: Mix of high-services (Denmark, Estonia, Belgium, Hong Kong,
          Greece, Croatia), manufacturing-driven (Germany, China, Japan), and
          rising IT-services (India, France as mid-tier)
        - **Excluded**: Ireland (140%+ due to MNC profit-booking distortion, not real services)
        - **Time range**: 1995-2023 to capture post-GATS/WTO services liberalization era
        - **Story**: Services economies cluster 30-65%; manufacturing economies stay below 25%;
          India's IT services growing from 5% to 15%; China and Japan remain low
        """
    )
    return


@app.cell
def _(json, by_country):
    label_map = {"Hong Kong SAR, China": "Hong Kong"}
    chart_data = []
    for c, pts in sorted(by_country.items()):
        pts_sorted = sorted(pts, key=lambda x: x["year"])
        chart_data.append({
            "n": label_map.get(c, c),
            "s": [round(p["value"], 1) for p in pts_sorted],
            "y0": pts_sorted[0]["year"]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
