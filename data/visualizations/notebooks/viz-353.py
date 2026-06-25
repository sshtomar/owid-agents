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
        # Youth Population Share 1990 vs 2022 -- Methodology

        Slope chart comparing children ages 0-14 as % of total population in 1990
        and 2022 for a diverse set of countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-0014-TO-ZS.json"
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
    keep = {'Chad','Congo, Dem. Rep.','Angola','Afghanistan','Cameroon','Ethiopia','Kenya',
            'Ghana','Egypt, Arab Rep.','Bolivia','Bangladesh','India','Indonesia',
            'Iran, Islamic Rep.','Colombia','Brazil','Australia','China','France',
            'Germany','Italy','Japan','Korea, Rep.'}
    by_country = defaultdict(dict)
    for p in data:
        if p['country'] not in agg_codes and p['value'] is not None and p['countryName'] in keep:
            by_country[p['countryName']][p['year']] = round(p['value'], 1)
    rows = []
    name_map = {'Egypt, Arab Rep.': 'Egypt', 'Iran, Islamic Rep.': 'Iran', 'Korea, Rep.': 'South Korea', 'Congo, Dem. Rep.': 'DR Congo'}
    for name, years in by_country.items():
        if 1990 in years and 2022 in years:
            rows.append({'n': name_map.get(name, name), 'a': years[1990], 'b': years[2022]})
    rows.sort(key=lambda x: -x['b'])
    print(f"Rows: {len(rows)}")
    return agg_codes, by_country, keep, name_map, rows


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- clear 1990 vs 2022 comparison
        - **Color**: by magnitude of decline (larger falls = greener)
        - **Story**: Sub-Saharan Africa still at 40-47% youth; Iran had one of history's
          fastest transitions (44%->23%); South Korea at 11.4% and Japan at 11.9%
          face severe aging; India and Bangladesh now transitioning rapidly
        """
    )
    return


@app.cell
def _(json, rows):
    print(json.dumps(rows, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
