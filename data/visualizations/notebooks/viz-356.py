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
        # Researchers in R&D Per Million People -- Methodology

        Trend lines for researchers in R&D (per million people) for selected countries,
        showing the knowledge-economy workforce evolution from 1996 to 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-SCIE-RD-P6.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    agg_codes = {'1A','1W','4E','7E','8S','B8','EU','F1','OE','S1','S2','S3','S4',
                 'T2','T3','T4','T5','T6','T7','V1','V2','V3','V4','XC','XD','XE',
                 'XF','XG','XH','XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU',
                 'Z4','Z7','ZF','ZG','ZH','ZI','ZJ','ZQ','ZT'}
    keep = {'Korea, Rep.', 'Denmark', 'Finland', 'Japan', 'Germany', 'Canada', 'France', 'China'}
    name_fix = {'Korea, Rep.': 'South Korea'}
    by_country = defaultdict(dict)
    for p in data:
        if p['country'] not in agg_codes and p['value'] is not None and p['countryName'] in keep:
            by_country[p['countryName']][p['year']] = round(p['value'])
    chart_data = []
    for name, years in sorted(by_country.items()):
        pts = [(y, v) for y, v in sorted(years.items()) if 1996 <= y <= 2023 and (y - 1996) % 2 == 0]
        chart_data.append({'n': name_fix.get(name, name), 'pts': [{'y': y, 'v': v} for y, v in pts]})
    chart_data.sort(key=lambda x: -x['pts'][-1]['v'])
    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        print(f"  {s['n']}: {s['pts'][0]['v']} -> {s['pts'][-1]['v']}")
    return agg_codes, by_country, chart_data, keep, name_fix


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows evolution of research workforce intensity
        - **Countries**: 8 with long, consistent series from 1996-2023
        - **Story**: South Korea overtook Japan (~5x growth in 27 years, now 9,472/million);
          Denmark & Finland among world's most research-intensive; China growing fast
          but still below 2,000; Japan's stagnation contrasts with Korea's rise
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
