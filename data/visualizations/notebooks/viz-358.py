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
        # Energy Use per Capita — Methodology

        Energy use per capita in kilograms of oil equivalent. Covers all energy forms
        (fossil fuels, nuclear, renewables). Reveals large disparities between nations
        and trends in energy intensity over 1995-2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
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
                 'Euro','Developing']
    code_name = {p['country']: p['countryName'] for p in data if p['value'] is not None}
    agg_codes = {code for code, name in code_name.items() if any(kw in name for kw in AGG_NAMES)}
    country_pts = [p for p in data if p['value'] is not None and p['country'] not in agg_codes]
    print(f"Individual countries: {len(set(p['country'] for p in country_pts))}")
    return AGG_NAMES, agg_codes, code_name, country_pts


@app.cell
def _(country_pts, json):
    SELECTED = {
        'IS': 'Iceland',
        'CA': 'Canada',
        'FI': 'Finland',
        'KR': 'South Korea',
        'AU': 'Australia',
        'DE': 'Germany',
        'JP': 'Japan',
        'FR': 'France',
        'CN': 'China',
        'BR': 'Brazil',
        'IN': 'India',
    }
    Y0, Y1 = 1995, 2022

    series_data = []
    for code, label in SELECTED.items():
        pts_c = {p['year']: p['value'] for p in country_pts if p['country'] == code and Y0 <= p['year'] <= Y1}
        if len(pts_c) < 20:
            print(f"SKIP {code}: only {len(pts_c)} pts")
            continue
        years = list(range(Y0, Y1 + 1))
        raw_s = [pts_c.get(y) for y in years]
        filled = []
        last = None
        for v in raw_s:
            last = v if v is not None else last
            filled.append(round(last, 0) if last is not None else None)
        series_data.append({"n": label, "s": filled, "y0": Y0})

    print(f"Series: {len(series_data)}")
    for s in series_data:
        print(f"  {s['n']}: {s['s'][0]} -> {s['s'][-1]}")
    print(json.dumps(series_data, separators=(",", ":")))
    return SELECTED, Y0, Y1, series_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — tracks change over time for multiple countries
        - **Country selection**: Iceland (extreme outlier due to geothermal/aluminum smelting),
          wealthy nations (Canada, Finland, South Korea, Australia, Germany, Japan, France),
          and rising economies (China, Brazil, India)
        - **Time range**: 1995-2022 — captures the era of China's industrialization
        - **Highlights**: China tripled energy use; Iceland far outpaces all; Germany/Japan improving efficiency
        - **Color**: warm for high energy users, cool for low
        """
    )
    return


if __name__ == "__main__":
    app.run()
