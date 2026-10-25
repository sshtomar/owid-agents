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
        # Freshwater Withdrawal as % of Resources — Methodology

        Trend lines for 10 water-stressed countries showing annual freshwater withdrawal
        as a percentage of internal renewable freshwater resources (1970–2022).
        Values above 100% indicate unsustainable extraction.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-H2O-FWTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


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
    selected = ['Israel', 'Azerbaijan', 'Iraq', 'Jordan', 'Hungary',
                'Barbados', 'Algeria', 'Iran, Islamic Rep.', 'India', 'Afghanistan']
    for n in selected:
        if n in countries:
            yv = countries[n]
            years = sorted(yv.keys())
            print(f"{n}: {years[0]}-{years[-1]}, latest={yv[years[-1]]:.1f}%")
    return (countries,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows whether water stress is increasing over time,
          which is the key policy question. Some countries (Algeria) are on a sharp upward
          trajectory; others (Israel) have stabilized through desalination.
        - **Country selection**: Top water-stressed countries excluding extreme outliers
          (Egypt at 7750%, Bahrain at 3877%) which would distort the scale. The selected
          10 span a range from 40% to 240%, all above safe ecological thresholds.
        - **Color encoding**: By latest withdrawal level (red = critical >150%, orange = high >100%).
        - **100% threshold line**: Key visual anchor — crossing 100% means a country uses more
          than nature replenishes annually; the deficit comes from fossil aquifers or external
          sources.
        - **Story**: Israel has declined from 237% to ~180% (desalination). Algeria is on a
          steep upward trajectory driven by agriculture. Iraq fluctuates with the Tigris-Euphrates
          flow. Jordan is chronically above 100%.
        """
    )
    return


if __name__ == "__main__":
    app.run()
