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
        # Energy Intensity of GDP — Methodology

        Trend lines for 10 major economies showing energy intensity (MJ per $2021 PPP GDP),
        2000-2022. Data source: World Bank EG.EGY.PRIM.PP.KD.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-EGY-PRIM-PP-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries_raw = {}
    for p in data:
        n = p["countryName"]
        v = p["value"]
        y = p["year"]
        if v is None:
            continue
        if n not in countries_raw:
            countries_raw[n] = {}
        countries_raw[n][y] = v

    target = {
        "China": "China", "Canada": "Canada", "Australia": "Australia",
        "India": "India", "Japan": "Japan", "Germany": "Germany",
        "France": "France", "Korea, Rep.": "South Korea",
        "Indonesia": "Indonesia", "Brazil": "Brazil",
    }

    result = []
    for code, display in target.items():
        if code not in countries_raw:
            continue
        series = [
            (y, round(countries_raw[code][y], 2))
            for y in sorted(countries_raw[code].keys())
            if 2000 <= y <= 2022
        ]
        if series:
            vals = [v for _, v in series]
            yr0 = series[0][0]
            result.append({"n": display, "s": vals, "y0": yr0, "step": 1})
            print(f"{display}: {vals[0]:.2f} -> {vals[-1]:.2f}")
    return (result,)


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
