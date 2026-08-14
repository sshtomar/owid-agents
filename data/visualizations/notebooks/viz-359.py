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
        # Old-Age Dependency Ratio (1960-2024) -- Methodology

        Trend lines showing the old-age dependency ratio for contrasting countries.
        The ratio = (population 65+) / (working-age population 15-64) * 100.
        A rising ratio means fewer workers supporting more retirees.
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
    by_cc = {}
    for r in data:
        by_cc.setdefault(r["country"], []).append(r)
    selected = ["JP","IT","DE","GR","FR","KR","CN","RU","BR","US","IN","ID","NG","ET"]
    years = list(range(1960, 2025, 5))
    chart_data = []
    for cc in selected:
        pts = by_cc.get(cc, [])
        if not pts:
            continue
        series = []
        for y in years:
            p = next((r for r in pts if r["year"]==y), None)
            series.append(round(p["value"],1) if p and p["value"] is not None else None)
        chart_data.append({"n": pts[0]["countryName"], "s": series, "y0": 1960, "step": 5})
    for c in chart_data:
        vals = [v for v in c["s"] if v is not None]
        print(f"  {c['n']}: {vals[0]:.1f}% (1960) -> {vals[-1]:.1f}% (latest)")
    return (chart_data, years, selected, by_cc)


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
