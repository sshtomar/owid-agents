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
        # International Tourism Arrivals — Methodology

        Number of international tourist arrivals per year. The 2020 data captures
        the COVID-19 collapse — a near-total halt to international travel.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
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
        'CN': 'China', 'IT': 'Italy', 'HR': 'Croatia',
        'DE': 'Germany', 'CA': 'Canada', 'HU': 'Hungary', 'AT': 'Austria',
    }
    Y0, Y1 = 2000, 2020

    series_data = []
    for code, label in SELECTED.items():
        pts_c = {p['year']: p['value'] for p in country_pts if p['country'] == code and Y0 <= p['year'] <= Y1}
        if len(pts_c) < 18:
            continue
        years = list(range(Y0, Y1 + 1))
        raw_s = [pts_c.get(y) for y in years]
        filled = []
        last = None
        for v in raw_s:
            last = v if v is not None else last
            filled.append(round(last / 1e6, 2) if last is not None else None)
        series_data.append({"n": label, "s": filled, "y0": Y0})

    print(f"Series: {len(series_data)}")
    for s in series_data:
        print(f"  {s['n']}: {s['s'][0]}M -> {s['s'][-1]}M (2020)")
    print(json.dumps(series_data, separators=(",", ":")))
    return SELECTED, Y0, Y1, series_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the build-up to 2019 peak and COVID collapse
        - **Country selection**: Major tourist destinations with full 2000-2020 coverage
        - **Y axis**: millions of arrivals
        - **Key insight**: China's arrivals fell 81% from 163M (2019) to 30M (2020);
          Italy fell 60%; all destinations collapsed in 2020
        - **Color**: warm for highest-volume destinations
        """
    )
    return


if __name__ == "__main__":
    app.run()
