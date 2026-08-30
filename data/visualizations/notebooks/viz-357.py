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
        # Nuclear Share of Electricity — Methodology

        Slope chart comparing 1990 vs 2024 nuclear electricity share (% of total) for 15 countries.
        Data source: World Bank EG.ELC.NUCL.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
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
        "France": "France", "Hungary": "Hungary", "Belgium": "Belgium",
        "Czechia": "Czechia", "Bulgaria": "Bulgaria", "Finland": "Finland",
        "Korea, Rep.": "South Korea", "Armenia": "Armenia", "Belarus": "Belarus",
        "Canada": "Canada", "Japan": "Japan", "Argentina": "Argentina",
        "India": "India", "China": "China", "Germany": "Germany",
    }

    result = []
    for code, display in target_map.items():
        if code not in countries:
            continue
        a = countries[code].get(1990) or countries[code].get(1991) or 0
        b = countries[code].get(2024) or countries[code].get(2023) or countries[code].get(2022) or 0
        if a > 0.5 or b > 0.5:
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
