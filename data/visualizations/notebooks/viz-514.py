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
        # Coal Rents (% of GDP) -- Methodology

        Documents the data pipeline for the coal rents visualization.
        Shows how coal-producing economies have depended on coal revenue,
        and how that has shifted as energy transition accelerates.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-COAL-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1980 and d["year"] <= 2021]
    countries = ["China", "Kazakhstan", "Indonesia", "India", "Australia", "Colombia"]
    by_country = {}
    for row in filtered:
        if row["countryName"] in countries:
            by_country.setdefault(row["countryName"], []).append(row)
    for c, pts in by_country.items():
        pts_sorted = sorted(pts, key=lambda x: x["year"])
        vals = [p["value"] for p in pts_sorted]
        print(f"{c}: {pts_sorted[0]['year']}-{pts_sorted[-1]['year']}, max={max(vals):.2f}%")
    return by_country, countries, filtered


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows how coal revenues peaked with 2008 commodity boom
          and declined post-2012 as renewables became competitive
        - **Country selection**: China (largest consumer/producer), Kazakhstan, Indonesia, India,
          Australia, Colombia -- the major coal economies that report data
        - **Time range**: 1980-2021, captures two commodity supercycles
        - **Story**: All coal economies saw a spike in 2008 then gradual decline. China's
          early peak (1982 high then fall as coal was subsidized) is notable. The 2008 spike
          across all countries shows the global commodity boom.
        - **Y-axis**: Max ~5% -- coal rents are much smaller than oil rents
        """
    )
    return


@app.cell
def _(json, by_country):
    chart_data = []
    order = ["China", "Kazakhstan", "Indonesia", "India", "Australia", "Colombia"]
    for c in order:
        pts = sorted(by_country.get(c, []), key=lambda x: x["year"])
        if pts:
            chart_data.append({
                "n": c,
                "s": [round(p["value"], 3) for p in pts],
                "y0": pts[0]["year"]
            })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
