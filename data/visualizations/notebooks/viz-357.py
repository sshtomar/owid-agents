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
        # Age Dependency Ratio 1960-2024 -- Methodology

        Documents the data pipeline for the trend-lines visualization of age dependency
        ratios across 8 countries from 1960 to 2024.
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
    PICKS = {
        "Japan": "Japan",
        "Germany": "Germany",
        "Korea, Rep.": "South Korea",
        "China": "China",
        "India": "India",
        "Brazil": "Brazil",
        "Egypt, Arab Rep.": "Egypt",
        "Ethiopia": "Ethiopia",
    }

    by_country = {}
    for r in data:
        cn = r["countryName"]
        if cn in PICKS:
            label = PICKS[cn]
            if label not in by_country:
                by_country[label] = {}
            if r["value"] is not None:
                by_country[label][r["year"]] = r["value"]

    out = []
    for label in PICKS.values():
        if label not in by_country:
            continue
        pts = by_country[label]
        years = list(range(1960, 2025, 4))
        series = []
        for y in years:
            v = pts.get(y)
            if v is not None:
                series.append({"y": y, "v": round(v, 1)})
        if series:
            latest = max(series, key=lambda x: x["y"])["v"]
            out.append({"n": label, "pts": series, "latest": latest})

    out.sort(key=lambda x: x["latest"], reverse=True)
    countries = [o["n"] for o in out]
    print(f"Countries: {countries}")
    return by_country, countries, out, PICKS


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows diverging paths over 64 years
        - **Country selection**: 8 countries representing rich aging societies (Japan, Germany),
          transitioning middle-income countries (South Korea, China, Brazil, Egypt, India),
          and a still-young high-fertility country (Ethiopia)
        - **Time range**: 1960-2024 every 4 years to keep data compact
        - **Story**: Japan rising from 55 to 70 while South Korea dropped to 37 then rebounded;
          China's dramatic fall driven by one-child policy; Ethiopia still above 73
        """
    )
    return


@app.cell
def _(json, out):
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
