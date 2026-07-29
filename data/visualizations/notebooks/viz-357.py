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
        # International Tourism Arrivals — Methodology

        Trend lines showing annual international tourist arrivals (millions) for 9 major
        destinations from 2000 to 2020. The dataset captures the COVID-19 collapse in 2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = {}
    for p in data:
        c = p["countryName"]
        if p["value"] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][p["year"]] = p["value"]
    print(f"Countries with data: {len(countries)}")
    return (countries,)


@app.cell
def _(countries):
    chosen = ["China", "Italy", "Hungary", "Croatia", "Hong Kong SAR, China",
              "Germany", "Greece", "Austria", "Japan"]
    chart_data = []
    for name in chosen:
        if name not in countries:
            continue
        vals = countries[name]
        pts = []
        for yr in range(2000, 2021):
            v = vals.get(yr)
            if v is not None:
                pts.append({"y": yr, "v": round(v / 1e6, 2)})
        v19 = vals.get(2019, 0)
        v20 = vals.get(2020, 0)
        drop = round((v20 / v19 - 1) * 100, 1) if v19 and v20 else 0
        display = name.replace("Hong Kong SAR, China", "Hong Kong")
        chart_data.append({"n": display, "drop": drop, "pts": pts})
    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        last = s["pts"][-1]
        print(f"  {s['n']}: 2020={last['v']}M ({s['drop']}% vs 2019)")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows continuous trajectory and the abrupt COVID shock
        - **Country selection**: Top destinations by 2019 arrivals with at least 20 data points
        - **Time range**: 2000–2020 to capture both the pre-COVID growth era and the 2020 collapse
        - **Color**: Diverging ramp by COVID-19 drop depth (biggest drop = darkest)
        - **Highlights**: Hong Kong -94%, Japan -87%, China -81% in a single year
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
