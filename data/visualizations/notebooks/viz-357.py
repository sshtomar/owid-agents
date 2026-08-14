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
        # International Tourism Arrivals (2000-2019) -- Methodology

        Trend lines showing how international tourist arrivals evolved across
        the world's top tourism destinations in the two decades before COVID-19.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGS = {"XD","OE","ZT","EU","XF","XO","XP","XC","XT","XN","ZJ","XU","XJ","ZH","ZI",
            "S3","B8","V2","Z4","7E","T4","Z7","ZQ","S2","S4","V4","1W","1A","4E","T7",
            "T5","T6","8S","ZG","ZF","XE","XM","XQ","XI","XG","XL","T2","T3","V1","V3","S1"}
    by_cc = {}
    for r in data:
        if r["country"] not in AGGS:
            by_cc.setdefault(r["country"], []).append(r)
    print(f"Countries (non-aggregate): {len(by_cc)}")
    return (by_cc, AGGS)


@app.cell
def _(by_cc):
    years = list(range(2000, 2020))
    selected = ["CN","IT","HK","HU","HR","CA","DE","AT","JP","IN","ID"]
    chart_data = []
    for cc in selected:
        pts = by_cc.get(cc, [])
        if not pts:
            continue
        series = []
        for y in years:
            p = next((r for r in pts if r["year"] == y), None)
            series.append(round(p["value"] / 1e6, 1) if p and p["value"] else None)
        name = pts[0]["countryName"]
        if name == "Hong Kong SAR, China":
            name = "Hong Kong"
        chart_data.append({"n": name, "s": series, "y0": 2000, "step": 1})
    print(f"Series count: {len(chart_data)}")
    for c in chart_data:
        print(f"  {c['n']}: max={max(v for v in c['s'] if v):.1f}M")
    return (chart_data, years, selected)


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
