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
        # HIV's Shifting Gender Balance — Methodology

        Documents the data pipeline behind viz-513: trend lines showing
        women's share of people living with HIV from 1990 to 2024 across
        selected regions and countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-AIDS-FE-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    non_null = [r for r in data if r["value"] is not None]
    targets = ["Angola","Sub-Saharan Africa","Ethiopia","Kenya","World","India","Arab World","Brazil"]

    series_map = {}
    for r in non_null:
        if r["countryName"] in targets:
            series_map.setdefault(r["countryName"], []).append((r["year"], round(r["value"], 1)))

    for name, pts in series_map.items():
        pts.sort()
        sampled = [p for p in pts if p[0] % 5 == 0]
        if pts and (not sampled or pts[-1][0] != sampled[-1][0]):
            sampled.append(pts[-1])
        print(f"{name}: {sampled[0]} -> {sampled[-1]}, {len(sampled)} points")
    return non_null, series_map, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the trajectory of gender composition of
          HIV over 34 years, revealing diverging regional paths
        - **Entity selection**: 4 African entities (Angola, Sub-Saharan Africa, Ethiopia,
          Kenya) to show the African feminization; World as a global reference; India and
          Brazil as non-African developing contexts; Arab World as a counter-example
          (women's share declining)
        - **Key story**: In Sub-Saharan Africa, the epidemic has steadily feminized from
          56% to 63% female, driven by biological vulnerability and gender inequality.
          The Arab World shows the opposite trend, driven by male-dominated transmission
          patterns (injecting drug use, labor migration).
        - **Reference line**: 50% gender parity line helps readers immediately see which
          regions have female-majority HIV populations
        """
    )
    return


@app.cell
def _(json, series_map):
    colors = {
        "Angola": "#EA5E33",
        "Sub-Saharan Africa": "#F29A44",
        "Ethiopia": "#C49A45",
        "Kenya": "#8BAD72",
        "World": "#2B2A27",
        "India": "#5B9E78",
        "Arab World": "#3D7A5A",
        "Brazil": "#A6C4A2"
    }
    chart_data = []
    for name, pts in series_map.items():
        sampled = sorted([p for p in pts if p[0] % 5 == 0])
        if pts and (not sampled or pts[-1][0] != sampled[-1][0]):
            sampled.append(sorted(pts)[-1])
        chart_data.append({
            "n": name,
            "pts": [{"y": y, "v": v} for y, v in sampled],
            "col": colors.get(name, "#9A9890")
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, colors


if __name__ == "__main__":
    app.run()
