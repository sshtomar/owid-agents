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
        # GNI per Capita PPP Slope Chart — Methodology

        Slope chart comparing 1990 vs 2024 GNI per capita (PPP, current int'l $).
        18 countries spanning low-income to high-income, highlighting economic convergence
        and divergence since 1990.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNP-PCAP-PP-CD.json"
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
        "Burundi": "Burundi", "Ethiopia": "Ethiopia", "Chad": "Chad",
        "Haiti": "Haiti", "Kenya": "Kenya", "Bolivia": "Bolivia",
        "Egypt, Arab Rep.": "Egypt", "Bangladesh": "Bangladesh",
        "India": "India", "Albania": "Albania", "Brazil": "Brazil",
        "Argentina": "Argentina", "China": "China", "Japan": "Japan",
        "Korea, Rep.": "South Korea", "Australia": "Australia",
        "Germany": "Germany", "Belgium": "Belgium",
    }

    slope = []
    for wbname, display in targets.items():
        if wbname not in by_country:
            continue
        a = by_country[wbname].get(1990)
        b = by_country[wbname].get(2024)
        if a and b:
            slope.append({"n": display, "a": round(a / 1000, 2), "b": round(b / 1000, 2)})

    slope.sort(key=lambda x: x["a"])
    for s in slope:
        ratio = s["b"] / s["a"]
        print(f"{s['n']}: ${s['a']}k -> ${s['b']}k (x{ratio:.1f})")
    return (slope,)


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
