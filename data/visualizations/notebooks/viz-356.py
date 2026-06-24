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
        # Anaemia in Non-Pregnant Women, 2000 vs 2023 -- Methodology

        Slope chart comparing the prevalence of anaemia among women aged 15-49 (excluding
        pregnant women) between 2000 and 2023. Shows both progress (many countries improving)
        and persistent gaps (South Asia, West Africa remain stubbornly high).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-NPRG-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(json, data):
    AGGREGATES = {'Arab World','East Asia & Pacific','Euro area','Europe & Central Asia','World','High income','Low income','Middle income','Latin America & Caribbean','Sub-Saharan Africa','Africa Eastern and Southern','Africa Western and Central','Low & middle income','OECD members','Upper middle income','Lower middle income','North America','Least developed countries: UN classification'}

    country_ts = {}
    for x in data:
        n = x['countryName']
        if n not in AGGREGATES and '(' not in n and 'excluding' not in n and x['value'] is not None:
            if n not in country_ts:
                country_ts[n] = {}
            country_ts[n][x['year']] = x['value']

    targets = ['Niger','Sierra Leone','Mali','Guinea','Burkina Faso','India','Bangladesh','Pakistan','Ethiopia','Afghanistan','Cambodia','Indonesia','Nigeria','South Africa','Brazil','Colombia','Peru','Mexico','United States','Germany','France','Finland','Australia','Japan']
    pairs = []
    for c in targets:
        if c not in country_ts:
            continue
        ts = country_ts[c]
        y2000, y2023 = ts.get(2000), ts.get(2023)
        if y2000 is not None and y2023 is not None:
            pairs.append({'n': c, 'a': round(y2000, 1), 'b': round(y2023, 1)})

    pairs.sort(key=lambda x: x['b'])
    print(json.dumps(pairs, separators=(',', ':')))
    return pairs, targets, country_ts


if __name__ == "__main__":
    app.run()
