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
        # Human Capital Index, 2010 vs 2020 -- Methodology

        Slope chart comparing Human Capital Index scores for 30 countries
        spanning the full distribution (top, middle, bottom) between 2010 and 2020.
        HCI measures the productivity a child born today can expect at age 18.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--HD-HCI-OVRL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_cc = {}
    for r in data:
        by_cc.setdefault(r["country"], []).append(r)
    pairs = []
    for cc, pts in by_cc.items():
        a = next((r for r in pts if r["year"]==2010), None)
        b = next((r for r in pts if r["year"]==2020), None)
        if a and b and a["value"] is not None and b["value"] is not None:
            pairs.append({"n": pts[0]["countryName"], "a": round(a["value"],3), "b": round(b["value"],3)})
    pairs.sort(key=lambda x: -x["b"])
    print(f"Countries with both years: {len(pairs)}")
    return (by_cc, pairs)


@app.cell
def _(pairs):
    total = len(pairs)
    top10 = pairs[:10]
    mid10 = pairs[total//2-5:total//2+5]
    bot10 = pairs[-10:]
    selected = top10 + mid10 + bot10
    print("Selected countries:")
    for p in selected:
        print(f"  {p['n']}: {p['a']:.3f} -> {p['b']:.3f}")
    return (selected, top10, mid10, bot10, total)


@app.cell
def _(json, selected):
    print(json.dumps(selected, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
