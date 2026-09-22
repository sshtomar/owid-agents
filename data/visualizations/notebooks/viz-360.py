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
        # Electricity from Natural Gas: 1990 vs 2023 — Methodology

        Documents the global shift in electricity generation mix toward (and away from) natural gas.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NGAS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {'ZH','ZI','S3','B8','V2','Z4','4E','T4','Z7','7E','T7','EU','XD','XF','ZT','XI','XG','V3','ZJ','XJ','T2','XL','XO','XN','XQ','T3','XP','XU','OE','S4','V4','V1','S1','8S','T5','ZG','ZF','T6','XT','1W','XE','XM','ZQ','M2','M1','XY','EA'}
    MICRO = {'GI', 'JE', 'GG', 'IM', 'BM', 'KY', 'VG', 'AW', 'CW', 'TC', 'FO', 'CX', 'CC'}

    countries = {}
    for r in data:
        if r['value'] is None: continue
        cc = r['country']
        if cc in AGGREGATES or cc in MICRO: continue
        if not cc.isalpha(): continue
        cn = r['countryName']
        if cc not in countries:
            countries[cc] = {'name': cn, 'pts': []}
        countries[cc]['pts'].append((r['year'], r['value']))

    results = []
    for cc, info in countries.items():
        pts = sorted(info['pts'], key=lambda x: x[0])
        yr1990 = next((v for y, v in pts if y == 1990), None)
        yr_recent = next((v for y, v in reversed(pts) if y >= 2020), None)
        if yr1990 is not None and yr_recent is not None:
            results.append({'n': info['name'], 'a': round(yr1990, 1), 'b': round(yr_recent, 1)})

    results.sort(key=lambda x: x['b'], reverse=True)
    print(f"Countries with 1990 and recent data: {len(results)}")
    return (countries, results)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares a single metric at two endpoints across many countries
        - **Country selection**: Mix of always-gas-heavy (Gulf states), new adopters (Israel, Jordan), and countries moving away (Finland, Bangladesh)
        - **Key insight**: Israel pivoted from 0% to 70% by developing its offshore Leviathan gas field; Finland moved from 8% to <1% by expanding renewables
        """
    )
    return


@app.cell
def _(json, results):
    KEEP = ['Bahrain', 'Algeria', 'Bangladesh', 'Israel', 'Jordan', 'Egypt, Arab Rep.', 'Argentina',
            'Ireland', 'Finland', 'Azerbaijan', 'Italy', 'Germany', 'France', 'Australia', 'Brazil']

    chart_data = [r for r in results if r['n'] in KEEP or any(k in r['n'] for k in ['Bahrain','Algeria','Bangladesh','Israel','Jordan','Egypt','Argentina','Ireland','Finland','Azerbaijan','Italy','Germany','France','Australia','Brazil'])]
    for r in chart_data:
        r['n'] = r['n'].replace('Egypt, Arab Rep.', 'Egypt').replace('United Kingdom', 'UK')
    chart_data.sort(key=lambda x: x['b'], reverse=True)
    print(f"Final: {len(chart_data)} countries")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
