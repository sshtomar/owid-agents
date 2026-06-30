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
        # Gross Fixed Capital Formation Slope Chart — Methodology

        Slope chart comparing 1990 vs 2022 GFCF as % of GDP for 14 countries.
        Shows China and Bangladesh's investment surge vs. Japan and Korea's decline.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NE-GDI-FTOT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_country = {}
    for p in data:
        if p["value"] is None:
            continue
        c = p["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][p["year"]] = p["value"]

    targets = {
        "China": "China", "Korea, Rep.": "Korea", "Japan": "Japan",
        "India": "India", "Bangladesh": "Bangladesh", "Brazil": "Brazil",
        "Germany": "Germany", "France": "France", "Ghana": "Ghana",
        "Argentina": "Argentina", "Chile": "Chile", "Australia": "Australia",
        "Iran, Islamic Rep.": "Iran", "Czechia": "Czechia",
    }

    slope = []
    for wbname, display in targets.items():
        if wbname not in by_country:
            continue
        a = by_country[wbname].get(1990)
        b = by_country[wbname].get(2022)
        if a and b and a > 0 and b > 0:
            slope.append({"n": display, "a": round(a, 1), "b": round(b, 1)})

    slope.sort(key=lambda x: x["a"])
    for s in slope:
        print(f"{s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f} pp)")
    return (slope,)


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
