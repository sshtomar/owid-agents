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
        # Energy Use per Capita, 1990 vs 2018 -- Methodology

        Slope chart comparing energy consumption per capita (kg of oil equivalent)
        between 1990 and 2018. Rich countries trend toward efficiency;
        rapidly industrializing economies surge upward.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
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
    # Curated selection: diverse mix of high/mid/low energy users with clear stories
    selected_cc = ["IS","CA","AU","KR","DE","FR","JP","CN","BR","EG","IN","BD"]
    pairs = []
    for cc in selected_cc:
        pts = by_cc.get(cc, [])
        if not pts:
            continue
        a = next((r for r in pts if r["year"]==1990), None)
        b = next((r for r in pts if r["year"]==2018), None)
        if a and b and a["value"] and b["value"]:
            pairs.append({"n": pts[0]["countryName"], "a": round(a["value"]), "b": round(b["value"])})
    pairs.sort(key=lambda x: -x["b"])
    for p in pairs:
        chg = (p["b"]-p["a"])/p["a"]*100
        print(f"  {p['n']}: {p['a']} -> {p['b']} ({chg:+.0f}%)")
    return (pairs, by_cc, selected_cc)


@app.cell
def _(json, pairs):
    print(json.dumps(pairs, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
