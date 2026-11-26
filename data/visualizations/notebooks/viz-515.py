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
        # Forest Area Loss and Gain -- Methodology

        Slope chart showing absolute forest area (million sq km) in 1990 vs 2022
        for the world's largest forested countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-LND-FRST-K2.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {
        "Brazil": "Brazil", "Canada": "Canada", "China": "China",
        "Congo, Dem. Rep.": "DR Congo", "Australia": "Australia",
        "Indonesia": "Indonesia", "India": "India", "Angola": "Angola",
        "Colombia": "Colombia", "Bolivia": "Bolivia",
        "Argentina": "Argentina", "Japan": "Japan", "Finland": "Finland",
    }
    result = []
    for orig, label in target.items():
        pts_map = {p["year"]: p["value"] for p in data if p["countryName"] == orig and p["value"] is not None}
        if 1990 in pts_map and 2022 in pts_map:
            a = round(pts_map[1990] / 1e6, 2)
            b = round(pts_map[2022] / 1e6, 2)
            result.append({"n": label, "a": a, "b": b})
    result.sort(key=lambda x: -x["a"])
    print(f"Countries: {len(result)}")
    for r in result:
        chg = r["b"] - r["a"]
        pct = chg / r["a"] * 100
        print(f"  {r['n']}: {r['a']} -> {r['b']} M sq km ({'+' if pct>=0 else ''}{pct:.1f}%)")
    return result, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — before/after comparison showing scale of gain or loss
        - **Country selection**: Top forest nations by absolute area in 1990
        - **Time range**: 1990 vs 2022 (32-year comparison)
        - **Color**: Brown/red for net loss, green for net gain, grey for stable
        - **Highlights**: Brazil lost 1.22M sq km (20%); China gained 650k sq km; DR Congo and Indonesia declining
        - **Units**: Million sq km (not %) to emphasize absolute scale of forest change
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
