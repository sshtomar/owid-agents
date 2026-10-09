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
        # Hydroelectric Share of Electricity — Methodology

        Trend lines from 1990 to 2024 showing the hydroelectric share of electricity
        for 10 nations that rely heavily on hydro power.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-HYRO-ZS.json"
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
    SELECTED = {'CD', 'ET', 'AL', 'CM', 'GE', 'AO', 'BR', 'CR', 'EC', 'AT'}
    NAME_MAP = {
        'CD': 'DR Congo', 'ET': 'Ethiopia', 'AL': 'Albania', 'CM': 'Cameroon',
        'GE': 'Georgia', 'AO': 'Angola', 'BR': 'Brazil', 'CR': 'Costa Rica',
        'EC': 'Ecuador', 'AT': 'Austria'
    }

    by_country = {}
    for row in data:
        cc = row.get('country', '')
        if cc not in SELECTED:
            continue
        year = row.get('year', 0)
        val = row.get('value')
        if val is None:
            continue
        if cc not in by_country:
            by_country[cc] = {'name': NAME_MAP.get(cc, cc), 'pts': {}}
        by_country[cc]['pts'][year] = round(val, 1)

    print("Selected countries:")
    for cc, info in by_country.items():
        pts = info['pts']
        print(f"  {info['name']}: {len(pts)} points, latest={pts[max(pts.keys())]:.1f}%")
    return by_country, AGGREGATES, SELECTED, NAME_MAP


@app.cell
def _(by_country):
    chart_data = []
    for cc, info in by_country.items():
        pts = info['pts']
        thinned = [
            {"y": y, "v": pts[y]}
            for y in sorted(pts.keys())
            if (y - 1990) % 3 == 0 or y == max(pts.keys())
        ]
        chart_data.append({"n": info["name"], "pts": thinned})
    chart_data.sort(key=lambda x: -x["pts"][-1]["v"])
    return chart_data,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — change over 1990–2024 for hydro-dependent nations
        - **Country selection**: Mix of near-100% dependent (DRC, Ethiopia) and declining (Brazil, Cameroon)
        - **Story**: Some nations diversifying away from hydro; others staying near 100%
        - **Sampling**: Every 3 years from 1990
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
