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
        # Scientific and Technical Journal Articles -- Methodology

        This notebook documents the data pipeline behind viz-362.
        Source: World Bank indicator IP.JRN.ARTC.SC
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-JRN-ARTC-SC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    # Top 8 countries by 2022 output, excluding regional aggregates
    exclude_kw = ["World","income","OECD","Euro","IDA","IBRD","dividend","poor","states",
                  "excluding","Blend","Arab","Africa","Asia","Latin","North America",
                  "Pacific","Caribbean","Central","Eastern","Western","Southern","Northern",
                  "Middle","Least","Sub-Saharan","classification","&"]
    def is_country(name):
        return not any(kw.lower() in name.lower() for kw in exclude_kw)

    yr2022 = [(p["countryName"], p["value"]) for p in data
              if p["year"] == 2022 and p["value"] is not None and is_country(p["countryName"])]
    yr2022.sort(key=lambda x: -x[1])
    top8_names = [n for n, _ in yr2022[:8]]
    print("Top 8:", top8_names)
    return exclude_kw, is_country, top8_names, yr2022


@app.cell
def _(data, json, top8_names):
    # Build time series: 2000-2022 every 2 years
    years = list(range(2000, 2023, 2))
    chart_data = []
    for name in top8_names:
        pts = sorted(
            [p for p in data if p["countryName"] == name and p["year"] in years and p["value"] is not None],
            key=lambda x: x["year"]
        )
        series = [round(p["value"] / 1000, 1) for p in pts]
        y0 = pts[0]["year"] if pts else 2000
        chart_data.append({"n": name, "s": series, "y0": y0, "step": 2})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, pts, years


if __name__ == "__main__":
    app.run()
