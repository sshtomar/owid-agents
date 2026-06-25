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
        # Anaemia Among Women of Reproductive Age, 2000 vs 2022 -- Methodology

        Slope chart showing prevalence of anaemia (%) among women ages 15-49
        for 27 countries, comparing 2000 to 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-ALLW-ZS.json"
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
    keep = {'Gabon','India',"Cote d'Ivoire",'Benin','Congo, Rep.','Chad','Gambia, The',
            'Guinea','Haiti','Afghanistan','Angola','Burkina Faso','Bangladesh',
            'Ghana','Egypt, Arab Rep.','Kenya','Indonesia','Iran, Islamic Rep.',
            'Ethiopia','Brazil','Japan','China','Germany','Canada','Finland',
            'France','Australia'}
    by_country = defaultdict(dict)
    for p in data:
        if p['country'] not in agg_codes and p['value'] is not None and p['countryName'] in keep:
            by_country[p['countryName']][p['year']] = round(p['value'], 1)
    name_fix = {'Egypt, Arab Rep.': 'Egypt', 'Iran, Islamic Rep.': 'Iran',
                "Cote d'Ivoire": "Cote d'Ivoire", 'Congo, Rep.': 'Congo', 'Gambia, The': 'Gambia'}
    rows = []
    for name, years in by_country.items():
        if 2000 in years and 2022 in years:
            rows.append({'n': name_fix.get(name, name), 'a': years[2000], 'b': years[2022]})
    rows.sort(key=lambda x: -x['b'])
    print(f"Rows: {len(rows)}")
    return agg_codes, by_country, keep, name_fix, rows


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- before/after comparison at two fixed points
        - **Country selection**: 27 countries from all burden categories
        - **Color**: warm if anaemia increased, cool if improved
        - **Story**: India is the most burdened major economy (53%); Afghanistan worsened;
          most West African countries improved; wealthy nations show small upticks
          possibly reflecting dietary surveys detecting borderline anaemia
        """
    )
    return


@app.cell
def _(json, rows):
    print(json.dumps(rows, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
