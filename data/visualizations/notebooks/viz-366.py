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
        # World Cereal Production — Methodology

        Trend lines for the top 10 cereal-producing nations from 1961 to 2024.
        Data sampled every 3 years to keep file size manageable.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-PRD-CREL-MT.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {
        'ZH','ZI','1A','S3','B8','V2','Z4','4E','T4','XC','Z7','7E','T7','EU','F2',
        'XE','XD','XF','ZT','XH','XI','XG','V3','ZJ','XJ','T2','XL','XO','XM','XN',
        'ZQ','XQ','T3','XP','XU','OE','S4','S2','V4','V1','S1','8S','T5','ZG','ZF',
        'T6','XT','1W'
    }
    by_country = {}
    for row in data:
        cc = row.get('country', '')
        if cc in AGGREGATES or len(cc) != 2:
            continue
        name = row.get('countryName', '')
        year = row.get('year', 0)
        val = row.get('value')
        if val is None:
            continue
        if cc not in by_country:
            by_country[cc] = {'name': name, 'pts': {}}
        by_country[cc]['pts'][year] = round(val / 1e6, 1)

    latest = {}
    for cc, info in by_country.items():
        yrs = sorted(info['pts'].keys())
        if yrs:
            latest[cc] = {'name': info['name'], 'val': info['pts'][yrs[-1]], 'pts': info['pts']}

    top10 = sorted(latest.values(), key=lambda x: -x['val'])[:10]
    print("Top 10 cereal producers (million metric tons, latest year):")
    for t in top10:
        print(f"  {t['name']}: {t['val']} Mt")
    return top10, latest, by_country, AGGREGATES


@app.cell
def _(top10):
    chart_data = []
    for t in top10:
        pts = t['pts']
        thinned = [
            {"y": y, "v": pts[y]}
            for y in sorted(pts.keys())
            if (y - 1961) % 3 == 0 or y == max(pts.keys())
        ]
        chart_data.append({"n": t["name"], "pts": thinned})
    return chart_data,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — long time series for multiple nations
        - **Country selection**: Top 10 by latest annual cereal production
        - **Units**: Million metric tons (divide raw values by 1,000,000)
        - **Sampling**: Every 3 years from 1961 to keep data compact
        - **Story**: China and India dominate; Brazil surge is driven by soy expansion
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
