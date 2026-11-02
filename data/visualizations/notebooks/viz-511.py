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
        # Net Primary School Enrollment by World Region -- Methodology

        Tracks the share of children of primary school age who are enrolled in
        primary education, across world regions, from 1970 to 2018.
        Source: World Bank indicator SE.PRM.NENR.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-NENR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    regions = [
        "Sub-Saharan Africa",
        "South Asia",
        "Arab World",
        "Latin America & Caribbean",
        "Europe & Central Asia",
        "High income",
        "Low income",
        "World",
    ]

    series = []
    for name in regions:
        if name not in by_country:
            continue
        pts = sorted(
            [{"y": yr, "v": round(v, 2)} for yr, v in by_country[name].items()
             if 1970 <= yr <= 2018],
            key=lambda x: x["y"]
        )
        if pts:
            series.append({"n": name, "pts": pts})
            print(f"{name}: {pts[0]['y']} ({pts[0]['v']}) -> {pts[-1]['y']} ({pts[-1]['v']})")
    return by_country, regions, series


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows how enrollment rates evolved over 50 years
        - **Region selection**: 8 world regions covering all income and geographic groups
        - **Time range**: 1970-2018 (most regions have continuous data in this window)
        - **Highlights**: Low-income countries made dramatic gains; Sub-Saharan Africa
          still lags; High income and Europe & Central Asia stayed consistently high
        """
    )
    return


@app.cell
def _(json, series):
    chart_data = series
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
