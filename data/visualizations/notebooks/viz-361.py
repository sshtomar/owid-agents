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
        # Primary School Completion Progress — Methodology

        Slope chart comparing circa 2000 vs most recent year primary school completion rate
        for 10 countries with large starting gaps, mostly in Sub-Saharan Africa and South/Southeast Asia.
        Data source: World Bank SE.PRM.CMPT.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
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

    target_map = {
        "Ghana": "Ghana", "India": "India", "Cambodia": "Cambodia",
        "Bhutan": "Bhutan", "Cote d'Ivoire": "Cote d'Ivoire",
        "Congo, Dem. Rep.": "D.R. Congo", "Guinea": "Guinea",
        "Ethiopia": "Ethiopia", "Burkina Faso": "Burkina Faso", "Chad": "Chad",
    }

    result = []
    for code, display in target_map.items():
        if code not in countries_raw:
            print(f"Missing: {code}")
            continue
        a = (countries_raw[code].get(2000) or countries_raw[code].get(2001)
             or countries_raw[code].get(2002))
        b = (countries_raw[code].get(2023) or countries_raw[code].get(2024)
             or countries_raw[code].get(2022) or countries_raw[code].get(2021)
             or countries_raw[code].get(2020))
        if a is not None and b is not None:
            result.append({"n": display, "a": round(a, 1), "b": round(b, 1)})

    result.sort(key=lambda x: -x["b"])
    for r in result:
        print(f"{r['n']}: {r['a']}% -> {r['b']}%")
    return (result,)


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
