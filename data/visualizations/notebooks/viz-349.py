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
        # Health Expenditure as % of GDP, 2000-2024 -- Methodology

        Trend lines showing how different countries allocate GDP to health spending,
        showing divergence between high-income and low-income countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-CHEX-GD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_codes = {'1A','1W','4E','7E','8S','B8','EU','F1','OE','S1','S2','S3','S4',
                 'T2','T3','T4','T5','T6','T7','V1','V2','V3','V4','XC','XD','XE',
                 'XF','XG','XH','XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU',
                 'Z4','Z7','ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','KP'}
    selected_codes = ['DE', 'FR', 'JP', 'AU', 'BR', 'CN', 'KR', 'ZA', 'EG', 'IN', 'ET', 'GH']
    country_pts = {}
    for r in data:
        if r['country'] in selected_codes and r['value'] is not None and r['year'] >= 2000:
            if r['country'] not in country_pts:
                country_pts[r['country']] = {'name': r['countryName'], 'pts': []}
            country_pts[r['country']]['pts'].append({'y': r['year'], 'v': round(r['value'], 2)})
    for c in country_pts:
        country_pts[c]['pts'].sort(key=lambda x: x['y'])
    result = [{'n': country_pts[code]['name'], 'pts': country_pts[code]['pts']} for code in selected_codes if code in country_pts]
    print(f"Selected {len(result)} countries")
    return agg_codes, country_pts, result, selected_codes


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows continuous change over time for multiple entities
        - **Country selection**: Diverse income levels -- rich (Germany, France, Japan, Australia),
          emerging (Brazil, China, Korea, South Africa), low (India, Ethiopia, Ghana, Egypt)
        - **Story**: South Korea doubled its health share in 24 years; Germany leads rich nations;
          India and Ethiopia spend a declining share despite growth
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
