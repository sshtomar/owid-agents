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
        # DPT Immunization Coverage by World Region — Methodology

        Documents the data pipeline and editorial decisions behind viz-357.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IDPT.json"
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
        "South Asia",
        "East Asia & Pacific",
        "Latin America & Caribbean",
        "Europe & Central Asia",
        "North America",
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
    from collections import defaultdict
    by_region = defaultdict(list)
    for row in filtered:
        by_region[row["countryName"]].append((row["year"], round(row["value"], 1)))

    chart_data = []
    for name, pts in by_region.items():
        label = label_map.get(name, name)
        chart_data.append({
            "n": label,
            "pts": [{"y": y, "v": v} for y, v in sorted(pts)]
        })
    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        pts = s["pts"]
        print(f"  {s['n']}: {pts[0]} -> {pts[-1]}")
    return by_region, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows 44 years of convergence/divergence across regions
        - **Entity selection**: 7 World Bank regional aggregates for clean comparison
        - **Time range**: 1980–2024 (full DPT data availability)
        - **Reference line**: 90% WHO target for childhood immunization coverage
        - **Color encoding**: Warm tones (red/orange/amber) for lower-coverage regions; cool tones for higher-coverage
        - **Key insight**: Africa West & Central started at 1.4% in 1980 and reached 74% by 2024 — a 50-fold increase.
          South Asia crossed 90% in 2017. The 2020–21 dip is visible in all regions due to COVID disruptions.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
