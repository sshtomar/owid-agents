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
        # Old-Age Dependency Ratio — Methodology

        Slope chart comparing 1990 vs 2024 old-age dependency ratio (people 65+ per 100
        working-age adults) for 12 countries. Data source: World Bank SP.POP.DPND.OL.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
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
        "Japan": "Japan", "Finland": "Finland", "Italy": "Italy",
        "Germany": "Germany", "France": "France", "Korea, Rep.": "South Korea",
        "China": "China", "Brazil": "Brazil", "India": "India",
        "Bangladesh": "Bangladesh", "Ethiopia": "Ethiopia", "Kenya": "Kenya",
    }

    result = []
    for code, display in target_map.items():
        if code not in countries:
            continue
        a = countries[code].get(1990)
        b = countries[code].get(2024)
        if a is not None and b is not None:
            result.append({"n": display, "a": round(a, 1), "b": round(b, 1)})

    result.sort(key=lambda x: -x["b"])
    for r in result:
        print(f"{r['n']}: {r['a']} -> {r['b']}")
    return (result,)


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
