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
        # Water Productivity — Methodology

        Slope chart comparing 2000 vs 2022 water productivity (constant 2015 USD per cubic
        meter of freshwater withdrawn) for 10 countries. Data source: World Bank ER.GDP.FWTL.M3.KD.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-GDP-FWTL-M3-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = {}
    for p in data:
        n = p["countryName"]
        v = p["value"]
        y = p["year"]
        if v is None:
            continue
        if n not in countries:
            countries[n] = {}
        countries[n][y] = v

    target_map = {
        "Israel": "Israel", "Germany": "Germany", "Australia": "Australia",
        "France": "France", "Japan": "Japan", "China": "China",
        "Brazil": "Brazil", "Egypt, Arab Rep.": "Egypt",
        "Indonesia": "Indonesia", "India": "India",
    }

    result = []
    for code, display in target_map.items():
        if code not in countries:
            continue
        a = countries[code].get(2000) or countries[code].get(2001)
        b = countries[code].get(2022) or countries[code].get(2021) or countries[code].get(2020)
        if a is not None and b is not None:
            result.append({"n": display, "a": round(a, 1), "b": round(b, 1)})

    result.sort(key=lambda x: -x["b"])
    for r in result:
        print(f"{r['n']}: ${r['a']} -> ${r['b']} per m³")
    return (result,)


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
