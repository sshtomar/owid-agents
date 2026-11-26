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
        # Services Sector as Share of GDP -- Methodology

        Trend lines of services value added (% of GDP) from 1980 to 2023,
        showing the structural transformation toward services-based economies.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-SRV-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {
        "Germany": "Germany", "Japan": "Japan", "France": "France",
        "China": "China", "India": "India", "Brazil": "Brazil",
        "Korea, Rep.": "South Korea", "Ethiopia": "Ethiopia", "Indonesia": "Indonesia",
    }
    years = [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023]
    result = []
    for orig, label in target.items():
        pts_map = {p["year"]: p["value"] for p in data if p["countryName"] == orig and p["value"] is not None}
        pts = [{"y": y, "v": round(pts_map[y], 1)} for y in years if y in pts_map]
        if len(pts) >= 5:
            result.append({"n": label, "pts": pts})
    for s in sorted(result, key=lambda x: -x["pts"][-1]["v"]):
        print(f"  {s['n']}: {s['pts'][0]['v']}% ({s['pts'][0]['y']}) -> {s['pts'][-1]['v']}% ({s['pts'][-1]['y']})")
    return result, target, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — services share evolves continuously over decades
        - **Country selection**: Mix of high-income (France, Germany, Japan) and emerging (China, India, Brazil, Korea)
        - **Time range**: 1980-2023 to capture the global services transformation
        - **Color**: Warm for high 2023 share, cool for low
        - **Highlights**: China rose from 22% to 56% — fastest structural shift of any major economy
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
