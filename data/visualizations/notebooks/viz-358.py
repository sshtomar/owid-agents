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
        # UHC Service Coverage Index — Methodology

        Slope chart comparing Universal Health Coverage index scores in 2000 vs 2023.
        The UHC index (0-100) measures access to essential health services across
        reproductive health, child health, infectious disease, and non-communicable disease.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--UHC_INDEX_REPORTED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    COUNTRY_NAMES = {
        'ETH': 'Ethiopia', 'MDG': 'Madagascar', 'NPL': 'Nepal',
        'COM': 'Comoros', 'BEN': 'Benin', 'PAK': 'Pakistan',
        'FSM': 'Micronesia', 'CPV': 'Cabo Verde', 'SWZ': 'Eswatini',
        'BIH': 'Bosnia & Herz.', 'JAM': 'Jamaica', 'MNG': 'Mongolia',
        'PRY': 'Paraguay', 'DZA': 'Algeria', 'ARG': 'Argentina',
        'CUB': 'Cuba', 'JOR': 'Jordan', 'CRI': 'Costa Rica',
        'BRB': 'Barbados', 'UZB': 'Uzbekistan', 'KWT': 'Kuwait',
        'BHS': 'Bahamas', 'GMB': 'Gambia', 'MRT': 'Mauritania',
        'SLE': 'Sierra Leone', 'VUT': 'Vanuatu', 'VEN': 'Venezuela',
        'MGL': 'Mongolia', 'SEN': 'Senegal', 'GHA': 'Ghana',
    }
    skip = {'AFR','AMR','EMR','EUR','SEAR','WPR','GLO','HIC','LIC','LMC',
            'UMC','WLD','GLOBAL','WB_LMI','WB_LMC','WB_UMC','WB_HIC'}
    countries = {}
    for row in data:
        cc = row['country']
        if cc in skip or 'UNSDG' in cc or 'UNICEF' in cc or 'WB_' in cc: continue
        if len(cc) != 3: continue
        yr = row['year']; val = row['value']
        if val is None: continue
        if cc not in countries: countries[cc] = {'code': cc, 'data': {}}
        countries[cc]['data'][yr] = val

    pairs = []
    for cc, info in countries.items():
        a = info['data'].get(2000)
        b = info['data'].get(2023) or info['data'].get(2022) or info['data'].get(2021)
        if a and b:
            name = COUNTRY_NAMES.get(cc, cc)
            pairs.append({'n': name, 'a': round(a), 'b': round(b)})

    pairs.sort(key=lambda x: x['a'])
    print(f"Countries in chart: {len(pairs)}")
    return countries, pairs, COUNTRY_NAMES


@app.cell
def _(json, pairs):
    print(json.dumps(pairs, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
