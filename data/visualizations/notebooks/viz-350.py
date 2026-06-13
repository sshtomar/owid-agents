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
        # Neonatal Mortality Sparkline Grid -- Methodology

        Compact grid showing neonatal mortality rate trends (1990-2023) for the
        24 countries with the highest current rates. Uses 5-year intervals.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-NMRT.json"
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
                 'Z4','Z7','ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','KP','DM'}
    country_data = {}
    for r in data:
        if r['country'] not in agg_codes and r['value'] is not None:
            if r['country'] not in country_data:
                country_data[r['country']] = {'name': r['countryName'], 'pts': {}}
            country_data[r['country']]['pts'][r['year']] = round(r['value'], 1)
    has_both = {c: info for c, info in country_data.items()
                if 2023 in info['pts'] and 1990 in info['pts']}
    sorted_2023 = sorted(has_both.items(), key=lambda x: -x[1]['pts'][2023])[:24]
    result = []
    for code, info in sorted_2023:
        years = list(range(1990, 2021, 5)) + [2023]
        series = [info['pts'].get(y) for y in years]
        if all(v is not None for v in series):
            result.append({'n': info['name'], 's': series, 'e': series[0], 'l': series[-1], 'y0': 1990})
    print(f"Final countries: {len(result)}")
    return agg_codes, country_data, has_both, result, sorted_2023


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid -- shows many trends compactly for visual scanning
        - **Country selection**: 24 highest neonatal mortality rate countries in 2023
        - **Ordering**: By 2023 rate (descending) -- tells the story of highest burden first
        - **Story**: Most countries improved, but Eswatini worsened (HIV impact then recovery)
        - **Botswana**: Notable HIV/AIDS bump visible in 2005-2015 before improvement
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
