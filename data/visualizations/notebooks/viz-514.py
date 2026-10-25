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
        # FDI Net Inflows 1990–2024 — Methodology

        Trend lines showing foreign direct investment net inflows as % of GDP for
        10 economies from 1990 to 2024. Data is 3-year smoothed to reduce
        year-to-year volatility from large one-time transactions.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--BX-KLT-DINV-WD-GD-ZS.json"
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
    selected = ['China', 'India', 'Brazil', 'Colombia', 'Ethiopia',
                'France', 'Germany', 'Argentina', 'Korea, Rep.', 'Indonesia']
    for n in selected:
        if n in countries:
            yv = countries[n]
            recent = [v for y, v in yv.items() if 2015 <= y <= 2023]
            avg = sum(recent)/len(recent) if recent else 0
            print(f"{n}: recent avg={avg:.2f}%")
    return (countries,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with 3-year smoothing — FDI is highly volatile
          (large M&A transactions can spike a country's value dramatically in a single year).
          Smoothing reveals structural trends rather than noise.
        - **Country selection**: Mix of emerging markets (China, India, Brazil, Colombia,
          Ethiopia, Indonesia) and developed economies (France, Germany, Argentina, Korea).
        - **Story**: China's peak FDI era was the mid-1990s when low wages attracted
          manufacturing. As wages rose, FDI as % GDP declined. India has maintained
          moderate, growing FDI. Ethiopia attracted significant FDI in the 2010s through
          special economic zones before political instability reduced inflows.
        - **Color encoding**: Country-specific distinct colors to aid line identification.
        """
    )
    return


if __name__ == "__main__":
    app.run()
