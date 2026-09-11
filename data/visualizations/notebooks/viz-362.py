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
    mo.md("# Primary School Completion Rate — Methodology\n\nTrend lines for regional aggregates, 1990–2024. Shows South Asia's dramatic gain and Sub-Saharan Africa's persistent gap. Data from World Bank SE.PRM.CMPT.ZS.")
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    regions = {"Sub-Saharan Africa": "Sub-Saharan Africa", "South Asia": "South Asia",
               "East Asia & Pacific": "East Asia & Pacific", "Latin America & Caribbean": "Latin America",
               "Arab World": "Arab World", "World": "World"}
    chart_data = []
    for r, label in regions.items():
        pts = sorted([(row["year"], round(row["value"], 1)) for row in data
                      if row["countryName"] == r and row["year"] >= 1990 and row["value"] is not None],
                     key=lambda x: x[0])
        if pts:
            chart_data.append({"n": label, "pts": [{"y": y, "v": v} for y, v in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
