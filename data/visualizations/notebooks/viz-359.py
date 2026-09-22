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
        # International Tourist Arrivals 2005–2020 — Methodology

        Documents the COVID-19 impact on global tourism.
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

    top_by_2019 = []
    for cc, info in countries.items():
        pts = {y: v for y, v in info['pts']}
        if 2019 in pts and 2020 in pts and 2005 in pts:
            top_by_2019.append((info['name'], cc, pts[2019], pts[2020]))
    top_by_2019.sort(key=lambda x: x[2], reverse=True)
    print("Top 15 by 2019 arrivals:")
    for name, cc, v19, v20 in top_by_2019[:15]:
        drop = (v20 - v19) / v19 * 100
        print(f"  {name}: {v19/1e6:.0f}M → {v20/1e6:.0f}M ({drop:.0f}%)")
    return (countries,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows both the growth decade 2005–2019 and the COVID cliff in 2020
        - **Country selection**: Top 10 destinations with data from 2005, covering Europe and Asia
        - **Key insight**: Growth was near-universal 2005–2019; the 2020 collapse varied dramatically — Hong Kong –94%, Japan –87%, France –46%, Hungary –48%
        - **Note**: World Bank figures count all border crossings; absolute values may exceed UNWTO overnight-stay counts for some countries
        """
    )
    return


@app.cell
def _(json, countries):
    TARGET_CCS = ['FR', 'CN', 'IT', 'HK', 'DE', 'GR', 'JP', 'AT', 'KR', 'HU']
    START, END = 2005, 2020

    chart_data = []
    for cc in TARGET_CCS:
        info = countries.get(cc)
        if not info: continue
        pts = {y: v for y, v in info['pts']}
        s = [round(pts[yr]/1e6, 2) if yr in pts else None for yr in range(START, END+1)]
        name = info['name'].replace('Hong Kong SAR, China', 'Hong Kong').replace('Korea, Rep.', 'South Korea')
        chart_data.append({'n': name, 'y0': START, 's': s})

    print(f"Series: {len(chart_data)}")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
