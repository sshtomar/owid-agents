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
        # Age Dependency Ratio, 1960-2020 -- Methodology

        Trend lines for 7 countries/regions showing the age dependency ratio
        (under-15 + over-64 as % of working-age population). Illustrates the
        demographic dividend and diverging aging trajectories.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_entity = defaultdict(list)
    for row in data:
        if row["value"] is not None and 1960 <= row["year"] <= 2020 and row["year"] % 5 == 0:
            by_entity[row["countryName"]].append((row["year"], row["value"]))

    selected = ["Sub-Saharan Africa", "South Asia", "India", "Brazil", "China",
                "Europe & Central Asia", "Japan"]
    series = {}
    for s in selected:
        pts = sorted(by_entity.get(s, []), key=lambda x: x[0])
        if pts:
            series[s] = pts
            print(f"{s}: {pts[0]} -> {pts[-1]}")
    return (by_entity, selected, series)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 5-year intervals reduce clutter across 60 years
        - **Entity selection**: Represents different demographic paths:
            - Sub-Saharan Africa: still very high, slow decline (high youth dependency)
            - South Asia / India / Brazil / China: dramatic dividend — ratios halved
            - Europe & Central Asia: aging up after 2005 (old-age dependency rising)
            - Japan: U-shaped — fell then reversed sharply (extreme aging)
        - **Time range**: 1960–2020 (5-year steps)
        - **Color**: Warm tones for high/falling ratios (dividend earners), cool for aging
        """
    )
    return


@app.cell
def _(json, series):
    chart_data = []
    for name, pts in series.items():
        chart_data.append({"n": name, "pts": [{"y": y, "v": round(v, 1)} for y, v in pts]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
