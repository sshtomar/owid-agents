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
        # Women's Share of HIV Population — Methodology

        Trend lines showing the feminization of HIV in Sub-Saharan Africa
        versus the global average and other regions.
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
    targets = ["Sub-Saharan Africa", "Africa Eastern and Southern", "Africa Western and Central",
               "World", "Angola", "Ghana", "Kenya", "Haiti", "Brazil", "India"]
    from collections import defaultdict
    by_entity = defaultdict(list)
    for row in data:
        n = row["countryName"]
        if n in targets and row["value"] is not None:
            by_entity[n].append((row["year"], row["value"]))

    for name in targets:
        vals = sorted(by_entity.get(name, []))
        if vals:
            v2023 = next((v for y, v in vals if y == 2023), None)
            v1990 = next((v for y, v in vals if y == 1990), None)
            print(f"{name}: {v1990:.1f}% (1990) -> {v2023:.1f}% (2023)")
    return by_entity, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how HIV gender composition shifted over three decades
        - **Entity selection**: Two sub-regional aggregates (the story), global reference line,
          and 6 individual countries for context (Angola, Ghana, Kenya, Haiti, Brazil, India)
        - **Time range**: 1990–2023 (full series)
        - **Highlights**: Africa W&C rose from 55.7% → 63.9%; Africa E&S from 55.6% → 62.3%;
          World inched from 46.9% → 53.2%; Brazil and India remain below 50%
        - **Reference line**: 50% parity line to show which regions exceed equal share
        """
    )
    return


@app.cell
def _(json, by_entity, targets):
    # Shorten regional names for display
    name_map = {
        "Africa Eastern and Southern": "Africa E. & Southern",
        "Africa Western and Central": "Africa W. & Central"
    }
    series = []
    for name in targets:
        pts_raw = sorted(by_entity.get(name, []))
        display_name = name_map.get(name, name)
        pts = [{"y": y, "v": round(v, 1)} for y, v in pts_raw if 1990 <= y <= 2023]
        if len(pts) >= 8:
            series.append({"n": display_name, "pts": pts})
    print(json.dumps(series, separators=(",", ":")))
    return series,


if __name__ == "__main__":
    app.run()
