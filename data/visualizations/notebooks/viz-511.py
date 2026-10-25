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
        # Clean Fuels for Cooking Access 2000→2024 — Methodology

        Slope chart comparing the share of population with access to clean
        cooking fuels in 2000 and 2024 for 17 developing countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-CFT-ACCS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    import re
    agg_codes = {'ZH','ZI','ZJ','ZQ','ZT','ZG','ZF','ZE','ZD','ZC','ZB','ZA','OE',
                 '1A','1W','4E','7E','8S','B8','S3','XC','XD','XE','XN','XO','XP','XQ','XT','XU','EU'}
    countries = {}
    for row in data:
        code = row['country']
        if code in agg_codes: continue
        if not re.match(r'^[A-Z]{2}$', code): continue
        if row['value'] is None: continue
        n = row['countryName']
        if n not in countries: countries[n] = {}
        countries[n][row['year']] = row['value']
    print(f"Individual countries: {len(countries)}")
    return (countries,)


@app.cell
def _(countries):
    selected = [
        'Burundi', 'Central African Republic', 'Ethiopia', 'Kenya', 'Chad',
        'Congo, Dem. Rep.', 'Guinea-Bissau', 'Cambodia', 'Djibouti',
        'Indonesia', 'Ghana', 'Bangladesh', 'Equatorial Guinea',
        "Cote d'Ivoire", 'India', 'Eswatini', 'Bhutan'
    ]
    chart_data = []
    for n in selected:
        if n not in countries: continue
        yv = countries[n]
        if 2000 not in yv: continue
        end_vals = {y: v for y, v in yv.items() if 2020 <= y <= 2024}
        if not end_vals: continue
        ey = max(end_vals.keys())
        chart_data.append({'n': n, 'a': round(yv[2000], 1), 'b': round(end_vals[ey], 1)})
    chart_data.sort(key=lambda x: x['a'])
    print(f"Chart countries: {len(chart_data)}")
    for cd in chart_data:
        print(f"  {cd['n']}: {cd['a']}% -> {cd['b']}% (+{cd['b']-cd['a']:.0f}pp)")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point comparison is the natural choice when the story
          is about change between a start and end year.
        - **Country selection**: Focused on developing countries with initially low access (<30%).
          Excluded countries already at >50% in 2000 (no interesting story). Included both
          fast movers (Indonesia, India, Bhutan) and stagnant cases (Burundi, CAR).
        - **Color encoding**: Diverging green (improvement) to red (stagnant) scale.
          Green = more households now have safe cooking fuel; red = still burning biomass.
        - **Story**: Indonesia is the standout (+84pp) via LPG subsidies. India's Ujjwala scheme
          drove +59pp. Sub-Saharan Africa largely stagnated.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
