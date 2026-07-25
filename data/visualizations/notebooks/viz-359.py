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
        # Population Ages 0–14 by World Region — Methodology

        Documents the data pipeline behind viz-359.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-0014-TO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    regions = [
        "Africa Western and Central",
        "Africa Eastern and Southern",
        "Sub-Saharan Africa",
        "South Asia",
        "East Asia & Pacific",
        "Latin America & Caribbean",
        "Europe & Central Asia",
        "World",
    ]
    label_map = {
        "Africa Western and Central": "Africa West & Central",
        "Africa Eastern and Southern": "Africa East & Southern",
        "Latin America & Caribbean": "Latin America",
    }
    filtered = [d for d in data if d["countryName"] in regions and d["value"] is not None]
    print(f"Filtered to {len(filtered)} regional data points")
    return filtered, label_map, regions


@app.cell
def _(filtered, label_map):
    # Subsample to 5-year intervals for cleaner chart data
    from collections import defaultdict
    by_region = defaultdict(dict)
    for row in filtered:
        by_region[row["countryName"]][row["year"]] = row["value"]

    target_years = [1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024]
    chart_data = []
    for name, ydict in by_region.items():
        label = label_map.get(name, name)
        pts = [(y, round(ydict[y], 1)) for y in target_years if y in ydict]
        chart_data.append({"n": label, "pts": [{"y": y, "v": v} for y, v in pts]})

    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        pts = s["pts"]
        print(f"  {s['n']}: {pts[0]} -> {pts[-1]}")
    return by_region, chart_data, target_years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — captures the long divergence story
        - **Entity selection**: 7 World Bank regional aggregates + World average
        - **Time range**: 1960–2024 (full availability)
        - **Key insight**: Sub-Saharan Africa (West and East) has barely changed since 1960 —
          youth share remains at 40–41%. East Asia dropped from 40% to 18% in 64 years.
          This divergence implies very different demographic futures: rapid aging in East Asia,
          continued population growth and youth bulge pressure in Sub-Saharan Africa.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
