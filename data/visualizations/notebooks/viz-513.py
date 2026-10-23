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
        # Hydropower Electricity Generation -- Methodology

        Trend lines showing hydropower generation (TWh) for the top 10 producing countries
        from 2000 to 2024. China's explosive growth stands out dramatically.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-HYDRO.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    top_countries = [
        "China", "Brazil", "Canada", "United States of America",
        "Russian Federation (the)", "India", "Norway", "Viet Nam",
        "Japan", "Turkey"
    ]
    name_map = {
        "United States of America": "United States",
        "Russian Federation (the)": "Russia",
        "Viet Nam": "Vietnam"
    }

    chart_data = []
    for c in top_countries:
        pts = [(r["year"], round(r["value"], 1)) for r in data
               if r["countryName"] == c and r["value"] is not None and 2000 <= r["year"] <= 2024]
        pts.sort()
        if len(pts) >= 15:
            label = name_map.get(c, c)
            chart_data.append({"n": label, "pts": [{"y": y, "v": v} for y, v in pts]})

    for cd in chart_data:
        print(f'{cd["n"]}: 2000={cd["pts"][0]["v"]}, 2024={cd["pts"][-1]["v"]} TWh')

    print()
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
