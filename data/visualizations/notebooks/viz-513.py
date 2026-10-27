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
        # Poverty Gap at $3/Day -- Methodology

        Documents the data pipeline for the poverty gap visualization.
        The poverty gap measures the average shortfall below the poverty
        line -- it captures how deep poverty is, not just how many are poor.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-POV-GAPS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1990]
    regions = ["Sub-Saharan Africa", "South Asia", "East Asia & Pacific",
               "Latin America & Caribbean", "World", "Europe & Central Asia"]
    by_region = {}
    for row in filtered:
        if row["countryName"] in regions:
            by_region.setdefault(row["countryName"], []).append(row)
    for r, pts in by_region.items():
        vals = [p["value"] for p in sorted(pts, key=lambda x: x["year"])]
        print(f"{r}: {len(pts)} pts, {vals[0]:.1f}% -> {vals[-1]:.1f}%")
    return by_region, regions


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- dramatic curves show where poverty has collapsed and
          where it remains stubborn
        - **Region selection**: Six World Bank regional aggregates. East Asia's drop from 30%
          to 0.4% is the central story (China's growth). Sub-Saharan Africa has barely moved.
        - **Time range**: 1990-2024, the era of the MDGs and SDGs
        - **Story**: Two diverging trajectories. East Asia and South Asia converged to near
          zero; Sub-Saharan Africa remains above 17%. Europe and Latin America near zero.
        - **Label shortening**: "Latin America & Caribbean" -> "Lat. Am. & Caribbean"
        """
    )
    return


@app.cell
def _(json, by_region):
    label_map = {
        "Latin America & Caribbean": "Lat. Am. & Carib.",
        "Europe & Central Asia": "Europe & C. Asia",
    }
    chart_data = []
    order = ["Sub-Saharan Africa", "East Asia & Pacific", "South Asia",
             "Latin America & Caribbean", "World", "Europe & Central Asia"]
    for r in order:
        pts = sorted(by_region.get(r, []), key=lambda x: x["year"])
        if pts:
            chart_data.append({
                "n": label_map.get(r, r),
                "s": [round(p["value"], 2) for p in pts],
                "y0": pts[0]["year"]
            })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
