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
    mo.md("# Manufacturing Value Added — Methodology\n\nTrend lines showing manufacturing as % of GDP for 8 countries, 1990–2024. Shows Western deindustrialisation (France, Italy) vs. Asian factory rise (Bangladesh, South Korea).")
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-MANF-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    focus = {"China": "China", "Germany": "Germany", "Japan": "Japan", "Korea, Rep.": "South Korea",
             "India": "India", "Brazil": "Brazil", "Bangladesh": "Bangladesh",
             "Italy": "Italy", "France": "France"}
    chart_data = []
    for c, label in focus.items():
        pts = sorted([(row["year"], round(row["value"], 2)) for row in data
                      if row["countryName"] == c and row["year"] >= 1990 and row["value"] is not None],
                     key=lambda x: x[0])
        if pts:
            chart_data.append({"n": label, "pts": [{"y": y, "v": v} for y, v in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
