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
        # Energy Use per Capita -- Sparkline Grid -- Methodology

        Dataset: wb--EG-USE-PCAP-KG-OE (World Bank, EG.USE.PCAP.KG.OE)
        Shows energy consumption per person in kg of oil equivalent for 20 diverse countries,
        1990-2020. Sorted by 2020 energy use (highest first).

        Design: Sparkline grid with 4 columns, each cell shows a country's
        trend line and latest value. Color: warm red = high energy use, green = low.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(data, json):
    selected = ['IS', 'BH', 'CA', 'FI', 'AU', 'BE', 'CZ', 'AT', 'KZ', 'DE',
                'IR', 'FR', 'CN', 'BR', 'ID', 'EG', 'IN', 'GH', 'ET', 'BD']
    by_country = {}
    for r in data:
        if r['country'] in selected and r['value'] is not None:
            code = r['country']
            if code not in by_country:
                by_country[code] = {'n': r['countryName'], 'v': {}}
            by_country[code]['v'][r['year']] = r['value']
    year_range = list(range(1990, 2021))
    sparklines = []
    for code in selected:
        if code in by_country:
            info = by_country[code]
            pts = info['v']
            vals = [round(pts[y], 0) if pts.get(y) else None for y in year_range]
            latest = round(pts.get(2020, pts.get(2019, 0)), 0)
            sparklines.append({"n": info['n'], "s": vals, "y0": 1990, "latest": int(latest)})
    sparklines.sort(key=lambda x: -x['latest'])
    print(json.dumps(sparklines))
    return sparklines, year_range


if __name__ == "__main__":
    app.run()
