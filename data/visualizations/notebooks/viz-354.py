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
        # Learning Poverty Rate -- Methodology

        Bar chart showing the share of children who cannot read a simple text by age 10
        (adjusted for out-of-school children), using the latest available year per country.
        Countries selected to span the full spectrum from near-zero to near-100%.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-LPV-PRIM.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(json, data):
    AGGREGATES = {'Arab World','East Asia & Pacific','Euro area','Europe & Central Asia','World','High income','Low income','Middle income','Latin America & Caribbean','Sub-Saharan Africa','Africa Eastern and Southern','Africa Western and Central','Low & middle income','OECD members','Upper middle income','Lower middle income','North America','Least developed countries: UN classification'}
    countries = {}
    for x in data:
        n = x['countryName']
        if n not in AGGREGATES and '(' not in n and 'excluding' not in n and x['value'] is not None:
            if n not in countries or x['year'] > countries[n]['year']:
                countries[n] = x
    recent = {c: v for c, v in countries.items() if v['year'] >= 2010}

    pick = ['Congo, Dem. Rep.','Burundi','Chad','Ethiopia','Cambodia','Guinea','Kenya','Honduras','Guatemala','Cameroon','Egypt, Arab Rep.','India','Indonesia','Colombia','Brazil','Hungary','Japan','Ireland']
    name_map = {'Congo, Dem. Rep.': 'DR Congo', 'Egypt, Arab Rep.': 'Egypt'}
    chart_data = [{"n": name_map.get(p, p), "v": round(recent[p]['value'], 1)} for p in pick if p in recent]
    chart_data.sort(key=lambda x: -x['v'])
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, name_map, pick, recent


if __name__ == "__main__":
    app.run()
