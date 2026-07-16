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
        # Electricity from Natural Gas -- Methodology

        Dataset: wb--EG-ELC-NGAS-ZS (World Bank, EG.ELC.NGAS.ZS)
        Shows the share of electricity production from natural gas sources
        for 18 countries, sampled every 5 years from 1990 to 2022.

        Design rationale:
        - Trend lines with color by 2022 share
        - Shows Middle East dependence on gas, Japan's post-Fukushima pivot,
          and European diversity
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NGAS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(data, json):
    target = {
        'AZ': 'Azerbaijan', 'BE': 'Belgium', 'BD': 'Bangladesh', 'DZ': 'Algeria',
        'EG': 'Egypt', 'ID': 'Indonesia', 'IR': 'Iran', 'IQ': 'Iraq',
        'IT': 'Italy', 'KZ': 'Kazakhstan', 'DE': 'Germany', 'CN': 'China',
        'IN': 'India', 'AR': 'Argentina', 'BH': 'Bahrain', 'JP': 'Japan',
        'FR': 'France', 'AU': 'Australia'
    }
    by_country = {}
    for r in data:
        if r['country'] in target and r['value'] is not None:
            code = r['country']
            if code not in by_country:
                by_country[code] = {'n': target[code], 'v': {}}
            by_country[code]['v'][r['year']] = r['value']
    years = list(range(1990, 2022, 5)) + [2022]
    series = []
    for code, info in by_country.items():
        pts = info['v']
        vals = [round(pts[y], 1) if pts.get(y) else None for y in years]
        last = round(pts.get(2022, pts.get(2021, 0)), 1)
        series.append({"n": info['n'], "s": vals, "y0": 1990, "step": 5, "last": last})
    series.sort(key=lambda x: -x['last'])
    print(json.dumps(series))
    return series, years


if __name__ == "__main__":
    app.run()
