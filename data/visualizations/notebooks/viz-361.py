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
        # Terrestrial Protected Areas, 2024 -- Methodology

        Horizontal bar chart showing the share of total land area designated
        as protected (national parks, reserves, etc.) for the top 25 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-LND-PTLD-ZS.json"
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
    AGGS = {"XD","OE","ZT","EU","XF","XO","XP","XC","XT","XN","ZJ","XU","XJ","ZH","ZI","S3","B8","V2","Z4","7E","T4","Z7","ZQ","S2","S4","V4","1W","1A","4E","T7","T5","T6","8S","ZG","ZF","XE","XM","XQ","XI","XG","XL","T2","T3","V1","V3","S1"}
    latest = []
    for cc, pts in by_cc.items():
        if cc in AGGS:
            continue
        for yr in range(2024, 2012, -1):
            p = next((r for r in pts if r["year"]==yr and r["value"] is not None), None)
            if p:
                latest.append({"cc": cc, "n": pts[0]["countryName"], "v": round(p["value"],1), "year": yr})
                break
    latest.sort(key=lambda x: -x["v"])
    print(f"Countries with recent data: {len(latest)}")
    print("Top 25:")
    for l in latest[:25]:
        print(f"  {l['n']}: {l['v']}% ({l['year']})")
    return (latest, by_cc, AGGS)


@app.cell
def _(json, latest):
    top25 = [{"n": x["n"], "v": x["v"]} for x in latest[:25]]
    print(json.dumps(top25, separators=(",", ":")))
    return (top25,)


if __name__ == "__main__":
    app.run()
