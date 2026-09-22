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
        # Intentional Homicide Rates 1990–2022 — Methodology

        Documents the data pipeline behind the homicide trend lines chart.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {'ZH','ZI','S3','B8','V2','Z4','4E','T4','Z7','7E','T7','EU','XD','XF','ZT','XI','XG','V3','ZJ','XJ','T2','XL','XO','XN','XQ','T3','XP','XU','OE','S4','V4','V1','S1','8S','T5','ZG','ZF','T6','XT','1W','XE','XM','ZQ','M2','M1','XY','EA'}

    countries = {}
    for r in data:
        if r['value'] is None: continue
        cc = r['country']
        if cc in AGGREGATES: continue
        if not cc.isalpha(): continue
        cn = r['countryName']
        if cc not in countries:
            countries[cc] = {'name': cn, 'pts': []}
        countries[cc]['pts'].append((r['year'], r['value']))

    print(f"Individual countries: {len(countries)}")
    return (countries,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows full temporal trajectory, not just endpoints
        - **Country selection**: Diverse stories — El Salvador (crisis then dramatic crackdown), Colombia (sustained decline), Ecuador (recent surge), Jamaica (persistently high), Japan/Germany (always very low)
        - **Time range**: 1990–2022 (El Salvador starts 1994)
        - **Key insight**: El Salvador peaked at 134/100k in 1995 and spiked again to 107 in 2015, then fell to 7.9 by 2022 — the sharpest drop in the dataset
        """
    )
    return


@app.cell
def _(json, countries):
    KEEP_CCS = ['EC', 'JM', 'HN', 'CO', 'SV', 'BR', 'CR', 'JP', 'DE', 'IT']
    START, END = 1990, 2022

    chart_data = []
    for cc in KEEP_CCS:
        info = countries.get(cc)
        if not info: continue
        pts = {y: v for y, v in info['pts']}
        s = [round(pts[yr], 1) if yr in pts else None for yr in range(START, END+1)]
        chart_data.append({'n': info['name'], 'y0': START, 's': s})

    print(f"Series: {len(chart_data)}")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
