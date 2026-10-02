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
        # Energy Use Per Capita 2000–2022 — Methodology

        Trend lines for 12 countries spanning the global income range.
        Illustrates the vast energy divide and China's remarkable rise.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for r in data:
        if r['value'] is not None:
            by_country[r['countryName']].append({'y': r['year'], 'v': r['value']})
    interest = ['Iceland','Canada','Korea, Rep.','Germany','France','Japan','Australia',
                'Brazil','China','Iran, Islamic Rep.','India','Bangladesh']
    name_map = {'Korea, Rep.': 'South Korea', 'Iran, Islamic Rep.': 'Iran'}
    series_data = []
    for cn in interest:
        pts = sorted([p for p in by_country.get(cn,[]) if 2000 <= p['y'] <= 2022], key=lambda x: x['y'])
        if pts:
            series_data.append({'name': name_map.get(cn,cn), 'pts': pts})
            print(f"  {name_map.get(cn,cn)}: {pts[0]['v']:.0f} → {pts[-1]['v']:.0f}")
    return series_data,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — continuous time series 2000-2022
        - **Countries**: 4 very high, 4 medium-high, 4 low-income — shows the full spectrum
        - **Story**: Iceland is uniquely high (geothermal industry); China tripled; Bangladesh barely grew
        - **Color**: Distinct palette per series, 12 lines
        """
    )
    return


@app.cell
def _(json, series_data):
    chart_data = [
        {"n": s['name'], "pts": [{"y": p['y'], "v": round(p['v'])} for p in s['pts']]}
        for s in series_data
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
