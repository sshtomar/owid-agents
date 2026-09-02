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
        # Scientific Journal Articles -- Methodology

        Documents the data pipeline for viz-360: trend lines showing scientific
        and technical journal article output for 11 major research nations,
        1996-2022. The headline story is China's extraordinary rise.
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
    SELECTED = {
        "China": "China", "India": "India", "Germany": "Germany",
        "Japan": "Japan", "Italy": "Italy", "Korea, Rep.": "South Korea",
        "Canada": "Canada", "France": "France", "Brazil": "Brazil",
        "Iran, Islamic Rep.": "Iran", "Australia": "Australia"
    }

    pts = [d for d in data if d["value"] is not None and d["countryName"] in SELECTED]
    print(f"Filtered to {len(pts)} data points across {len(SELECTED)} countries")
    return SELECTED, pts


@app.cell
def _(SELECTED, pts):
    countries = {name: {} for name in SELECTED.values()}
    for p in pts:
        name = SELECTED[p["countryName"]]
        countries[name][p["year"]] = round(p["value"], 0)

    years = list(range(1996, 2024))
    chart_data = []
    for orig, name in SELECTED.items():
        yv = countries.get(name, {})
        series = [yv.get(y) for y in years]
        while series and series[-1] is None:
            series.pop()
        chart_data.append({"n": name, "s": series, "y0": 1996, "step": 1})

    chart_data.sort(key=lambda x: (x["s"][-1] or 0), reverse=True)
    for c in chart_data:
        v1996 = c["s"][0] if c["s"] else 0
        vlast = c["s"][-1] if c["s"] else 0
        print(f"{c['n']}: 1996={v1996:,.0f}, latest={vlast:,.0f}")
    return chart_data, countries, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows China's explosive divergence from other nations
        - **Country selection**: 11 major research nations to show global science landscape
        - **Time range**: 1996-2022 (full NSF data coverage)
        - **Highlights**: China went from 34k articles in 1996 to 886k in 2022 (26x growth),
          surpassing all other nations combined except the US aggregate.
          India second fastest; Iran's rise from near-zero is notable.
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
