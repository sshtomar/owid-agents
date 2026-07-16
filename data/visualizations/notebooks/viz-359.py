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
        # Youth Dependency Ratio Slope Chart -- Methodology

        Dataset: wb--SP-POP-DPND-YG (World Bank, SP.POP.DPND.YG)
        Compares youth dependency ratio (children 0-14 per 100 working-age people)
        between 2000 and 2023 across 40 countries, sorted by 2023 value.
        Shows the persistent youth bulge in Sub-Saharan Africa vs demographic maturity
        in East Asia and Europe.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-YG.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(data, json):
    by_country = {}
    for r in data:
        if r['value'] is not None:
            code = r['country']
            if len(code) == 2 and code.isalpha() and code.upper() == code:
                if code not in by_country:
                    by_country[code] = {'n': r['countryName'], 'v': {}}
                by_country[code]['v'][r['year']] = r['value']

    target = ['CF', 'TD', 'CD', 'BI', 'AO', 'AF', 'BF', 'BJ', 'CM', 'GN',
              'CI', 'CG', 'GM', 'ET', 'GW', 'ER', 'KM', 'KE', 'IQ', 'GH',
              'EG', 'GT', 'BW', 'DZ', 'HN', 'BD', 'IN', 'ID', 'IR', 'CO',
              'BR', 'CN', 'GR', 'CZ', 'HU', 'DE', 'IT', 'FR', 'JP', 'KR']

    slopes = []
    for code in target:
        if code in by_country:
            info = by_country[code]
            v2000 = info['v'].get(2000)
            v2023 = info['v'].get(2023) or info['v'].get(2022)
            if v2000 and v2023:
                slopes.append({"n": info['n'], "a": round(v2000, 1), "b": round(v2023, 1)})

    slopes.sort(key=lambda x: -x['b'])
    print(f"Countries: {len(slopes)}")
    print(json.dumps(slopes))
    return slopes


if __name__ == "__main__":
    app.run()
