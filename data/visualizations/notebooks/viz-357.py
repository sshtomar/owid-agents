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
        # Old-Age Dependency Ratio: 1990 vs 2023 — Methodology

        Documents the data pipeline behind the aging slope chart.
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
    AGGREGATES = {'ZH','ZI','S3','B8','V2','Z4','4E','T4','Z7','7E','T7','EU','XD','XF','ZT','XI','XG','V3','ZJ','XJ','T2','XL','XO','XN','XQ','T3','XP','XU','OE','S4','V4','V1','S1','8S','T5','ZG','ZF','T6','XT','1W','XE','XM','ZQ','M2','M1','XY','EA'}
    MICRO = {'IM', 'BM', 'JE', 'GG', 'FO', 'GI', 'MC', 'SM', 'LI', 'AD', 'VA', 'KY', 'AW', 'CW', 'VG', 'AS', 'GU', 'PF'}

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
        yr2023 = next((v for y, v in pts if y == 2023), next((v for y, v in reversed(pts) if y >= 2020), None))
        if yr1990 is not None and yr2023 is not None:
            results.append({'n': info['name'], 'a': round(yr1990, 1), 'b': round(yr2023, 1)})

    results.sort(key=lambda x: x['b'], reverse=True)
    print(f"Countries with both 1990 and 2023 data: {len(results)}")
    return countries, results


@app.cell
def _(results):
    import statistics
    vals_a = [r['a'] for r in results]
    vals_b = [r['b'] for r in results]
    print(f"1990 range: {min(vals_a):.1f} - {max(vals_a):.1f}, median: {statistics.median(vals_a):.1f}")
    print(f"2023 range: {min(vals_b):.1f} - {max(vals_b):.1f}, median: {statistics.median(vals_b):.1f}")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points is ideal for slope; shows both absolute values and direction of change
        - **Country selection**: Top 15 by 2023 dependency ratio (predominantly European/East Asian) plus Brazil, China, India, Ethiopia for global context
        - **Key story**: Japan tripled its ratio (17→50); South Korea at 7→26 signals the next wave; African countries remain near zero
        - **Color encoding**: Change magnitude — warmest for largest jumps
        """
    )
    return


@app.cell
def _(json, results):
    KEEP = ['Japan', 'Finland', 'Italy', 'Greece', 'Croatia', 'Germany', 'France', 'Bulgaria',
            'Bosnia and Herzegovina', 'Estonia', 'Denmark', 'Czechia', 'Hungary',
            'Korea, Rep.', 'Australia', 'Canada', 'China', 'Brazil', 'India', 'Ethiopia']

    selected = [r for r in results if any(k in r['n'] for k in KEEP)]
    for r in selected:
        r['n'] = (r['n']
            .replace('Bosnia and Herzegovina', 'Bosnia & Herz.')
            .replace('Korea, Rep.', 'Korea')
            .replace('Hong Kong SAR, China', 'Hong Kong'))
    selected.sort(key=lambda x: x['b'], reverse=True)
    chart_data = selected[:20]
    print(f"Final chart data: {len(chart_data)} countries")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
