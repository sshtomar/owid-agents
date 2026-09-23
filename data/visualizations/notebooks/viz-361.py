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
        # Measles Immunization Coverage — Methodology

        Percentage of children ages 12-23 months immunized against measles.
        Shows the global vaccination progress from 1990-2023 with stark differences
        between countries that reached near-universal coverage and those still lagging.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-MEAS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGG_NAMES = ['Africa','Asia','Europe','America','Arab','Caribbean','OECD','Upper',
                 'Lower','Middle','High','Low','World','Small','East','West','South',
                 'North','Sub-','Pacific','income','dividend','states','countries',
                 'economies','union','Central','Fragile','Heavily','Least','Blend',
                 'Euro','Developing','IDA','IBRD','total']
    code_name = {p['country']: p['countryName'] for p in data if p['value'] is not None}
    agg_codes = {code for code, name in code_name.items() if any(kw in name for kw in AGG_NAMES)}
    country_pts = [p for p in data if p['value'] is not None and p['country'] not in agg_codes]
    print(f"Countries: {len(set(p['country'] for p in country_pts))}")
    return AGG_NAMES, agg_codes, code_name, country_pts


@app.cell
def _(country_pts, json):
    SELECTED = {
        'IN': 'India',
        'ID': 'Indonesia',
        'BD': 'Bangladesh',
        'ET': 'Ethiopia',
        'CD': 'DR Congo',
        'CN': 'China',
        'BR': 'Brazil',
        'DE': 'Germany',
    }
    Y0, Y1 = 1990, 2023

    series_data = []
    for code, label in SELECTED.items():
        pts_c = {p['year']: p['value'] for p in country_pts if p['country'] == code and Y0 <= p['year'] <= Y1}
        if len(pts_c) < 25:
            continue
        years = list(range(Y0, Y1 + 1))
        raw_s = [pts_c.get(y) for y in years]
        filled = []
        last = None
        for v in raw_s:
            last = v if v is not None else last
            filled.append(round(last, 1) if last is not None else None)
        series_data.append({"n": label, "s": filled, "y0": Y0})

    print(f"Series: {len(series_data)}")
    for s in series_data:
        print(f"  {s['n']}: {s['s'][0]}% -> {s['s'][-1]}%")
    print(json.dumps(series_data, separators=(",", ":")))
    return SELECTED, Y0, Y1, series_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectories and turning points over 34 years
        - **Country selection**: Mix of fast improvers (India: 56->93%, Bangladesh: 65->96%),
          laggards (DR Congo: 38->52%), already-high (China: 98%, Germany: 75->97%)
        - **Color**: Improvement bands — green for 37%+ gain, amber/red for stagnant
        - **Reference line**: WHO 95% target for herd immunity
        - **Key insight**: South Asian countries made dramatic gains; Sub-Saharan Africa lags
        """
    )
    return


if __name__ == "__main__":
    app.run()
