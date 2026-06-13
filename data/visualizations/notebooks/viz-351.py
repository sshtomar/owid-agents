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
        # Adult Male Mortality, 1990 vs 2023 -- Methodology

        Slope chart showing the change in adult male mortality rate (per 1,000 male adults)
        for the 25 highest-burden countries in 1990.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-AMRT-MA.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_codes = {'1A','1W','4E','7E','8S','B8','EU','F1','OE','S1','S2','S3','S4',
                 'T2','T3','T4','T5','T6','T7','V1','V2','V3','V4','XC','XD','XE',
                 'XF','XG','XH','XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU',
                 'Z4','Z7','ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','KP','GI','JE','FO','PF'}
    country_data = {}
    for r in data:
        if r['country'] not in agg_codes and r['value'] is not None:
            if r['country'] not in country_data:
                country_data[r['country']] = {'name': r['countryName'], 'pts': {}}
            country_data[r['country']]['pts'][r['year']] = round(r['value'], 1)
    has_both = {c: info for c, info in country_data.items()
                if 1990 in info['pts'] and 2023 in info['pts']}
    rows = sorted([
        {'n': info['name'], 'a': info['pts'][1990], 'b': info['pts'][2023]}
        for c, info in has_both.items()
    ], key=lambda x: -x['a'])[:25]
    print(f"Selected {len(rows)} countries")
    return agg_codes, country_data, has_both, rows


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- clear before/after comparison at two time points
        - **Country selection**: Top 25 by 1990 adult male mortality
        - **Color**: By % improvement -- green for large drops, red for worsening
        - **Story**: Iraq's 66% drop (post-conflict stability), Kenya and Eswatini worsened
          due to HIV/AIDS peak impact; Central African Republic barely improved at 5%
        """
    )
    return


@app.cell
def _(json, rows):
    print(json.dumps(rows, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
