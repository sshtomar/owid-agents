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
        # Electricity from Coal, 2000 vs 2022 -- Methodology

        Slope chart for countries that had >20% coal-powered electricity in 2000,
        showing who has decarbonized (Europe) vs who has not (South/Southeast Asia).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-COAL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(json, data):
    AGGREGATES = {'Arab World','East Asia & Pacific','Euro area','Europe & Central Asia','World','High income','Low income','Middle income','Latin America & Caribbean','Sub-Saharan Africa','Low & middle income','OECD members','Upper middle income','Lower middle income','North America','Least developed countries: UN classification','Small states','European Union'}

    country_ts = {}
    for x in data:
        n = x['countryName']
        if n not in AGGREGATES and '(' not in n and 'excluding' not in n and x['value'] is not None:
            if n not in country_ts:
                country_ts[n] = {}
            country_ts[n][x['year']] = x['value']

    pairs = []
    exclude = {"Korea, Dem. People's Rep."}
    for c, ts in country_ts.items():
        if c in exclude:
            continue
        y2000 = ts.get(2000)
        y2022 = ts.get(2022) or ts.get(2021)
        if y2000 is not None and y2022 is not None and y2000 > 20:
            name = c.replace("Korea, Rep.", "South Korea").replace("Bosnia and Herzegovina", "Bosnia & Herz.")
            pairs.append({'n': name, 'a': round(y2000, 1), 'b': round(y2022, 1)})

    pairs.sort(key=lambda x: x['b'])
    # Drop small aggregates
    pairs = [p for p in pairs if p['n'] not in {'Small states', 'European Union', 'Hong Kong SAR, China'}]
    print(json.dumps(pairs, separators=(',', ':')))
    return pairs, country_ts


if __name__ == "__main__":
    app.run()
