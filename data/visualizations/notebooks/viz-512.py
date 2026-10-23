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
        # Electricity Demand Per Capita -- Methodology

        Trend lines chart showing electricity consumption per person (MWh) from 2000 to 2024
        for 17 major economies. Reveals the dramatic development gap and China's surge.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--DEMAND-PER-CAPITA.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    target = [
        "United States of America", "China", "India", "Germany", "Brazil", "Japan",
        "France", "Nigeria", "Bangladesh", "South Korea", "United Kingdom",
        "South Africa", "Indonesia", "Mexico", "Canada", "Pakistan", "Egypt"
    ]
    name_map = {
        "United States of America": "United States", "South Korea": "Korea",
        "United Kingdom": "UK", "South Africa": "S. Africa"
    }

    chart_data = []
    for c in target:
        pts = [(r["year"], round(r["value"], 2)) for r in data
               if r["countryName"] == c and r["value"] is not None and 2000 <= r["year"] <= 2024]
        pts.sort()
        if len(pts) >= 15:
            label = name_map.get(c, c)
            v0 = pts[0][1]
            vn = pts[-1][1]
            pct_change = round((vn - v0) / v0 * 100, 0)
            chart_data.append({
                "n": label,
                "pts": [{"y": y, "v": v} for y, v in pts],
                "pct": pct_change
            })

    chart_data.sort(key=lambda x: x["pts"][-1]["v"], reverse=True)
    for cd in chart_data:
        print(f'{cd["n"]}: 2000={cd["pts"][0]["v"]}, 2024={cd["pts"][-1]["v"]} (+{cd["pct"]}%)')
    print()
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
