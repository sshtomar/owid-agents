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
        # The Services Economy: Sector Share of GDP Across Economies -- Methodology

        Trend lines showing services value added as a percentage of GDP for a diverse
        set of countries from 1960 to 2024. Illustrates structural economic transformation
        as countries develop from agriculture-dominated to services-dominated economies.
        Source: World Bank indicator NV.SRV.TOTL.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-SRV-TOTL-ZS.json"
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
        if row["value"] is not None and row["value"] > 5:  # exclude bad 0 values
            by_country[row["countryName"]][row["year"]] = row["value"]

    target = [
        "France", "Korea, Rep.", "China", "India",
        "Bangladesh", "Botswana", "Costa Rica", "Ecuador",
    ]

    series = []
    for name in target:
        if name not in by_country:
            print(f"MISSING: {name}")
            continue
        pts = sorted(
            [{"y": yr, "v": round(v, 1)} for yr, v in by_country[name].items()
             if 1960 <= yr <= 2024],
            key=lambda x: x["y"]
        )
        if len(pts) >= 15:
            series.append({"n": name, "pts": pts})
            print(f"{name}: {pts[0]['y']} ({pts[0]['v']}) -> {pts[-1]['y']} ({pts[-1]['v']})")
    return by_country, series, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- best for comparing structural change over 60 years
        - **Country selection**: France (mature service economy), Korea (industrial transition),
          China (manufacturing giant adding services), India and Bangladesh (services-led
          development), Botswana (diversification), Costa Rica and Ecuador (Latin American paths)
        - **Time range**: 1960-2024
        - **Highlights**: France rose from 47% to 71%; China from 33% to 57%; India remains
          comparatively low at 48% despite its IT sector fame
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
