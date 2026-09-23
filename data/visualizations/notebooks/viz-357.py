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
        # Old-Age Dependency Ratio — Methodology

        How many retirees (65+) does each working-age adult (15-64) support?
        This notebook extracts and shapes the data for the trend-lines visualization.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATES = {
        'AFE','AFW','ARB','CSS','CEB','EAP','EAR','EAS','ECA','ECS','EMU','EUU',
        'FCS','HIC','HPC','IBD','IBT','IDA','IDB','IDX','LAC','LCN','LDC','LMC',
        'LMY','LTE','MEA','MIC','MNA','NAC','OED','OSS','PRE','PSS','PST','SAS',
        'SSA','SSF','SST','TEA','TEC','TLA','TMN','TSA','TSS','UMC','WLD','1W',
        'ZH','ZI','Z4','Z7','ZF','ZG','ZJ','ZQ','ZT','ZW',
    }
    AGG_NAMES = ['Africa','Asia','Europe','America','Arab','Caribbean','OECD','Upper',
                 'Lower','Middle','High','Low','World','Small','East','West','South',
                 'North','Sub-','Pacific','income','dividend','states','countries',
                 'economies','union','Central','Fragile','Heavily','Least','Blend',
                 'Euro','Developing']

    code_name = {p['country']: p['countryName'] for p in data if p['value'] is not None}
    agg_codes = AGGREGATES | {
        code for code, name in code_name.items()
        if any(kw in name for kw in AGG_NAMES)
    }
    country_pts = [p for p in data if p['value'] is not None and p['country'] not in agg_codes]
    print(f"After filtering aggregates: {len(set(p['country'] for p in country_pts))} countries")
    return AGG_NAMES, AGGREGATES, agg_codes, code_name, country_pts


@app.cell
def _(country_pts):
    SELECTED = {
        'JP': 'Japan',
        'KR': 'South Korea',
        'IT': 'Italy',
        'DE': 'Germany',
        'FR': 'France',
        'CN': 'China',
        'BR': 'Brazil',
        'IN': 'India',
        'ET': 'Ethiopia',
    }
    Y0, Y1 = 1980, 2023

    series_data = []
    for code, label in SELECTED.items():
        pts_c = {p['year']: p['value'] for p in country_pts if p['country'] == code and Y0 <= p['year'] <= Y1}
        if len(pts_c) < 30:
            print(f"SKIP {code}: only {len(pts_c)} points")
            continue
        years = list(range(Y0, Y1 + 1))
        raw_s = [pts_c.get(y) for y in years]
        filled = []
        last = None
        for v in raw_s:
            last = v if v is not None else last
            filled.append(round(last, 2) if last is not None else None)
        series_data.append({"n": label, "s": filled, "y0": Y0})

    print(f"Series: {len(series_data)}")
    for s in series_data:
        print(f"  {s['n']}: {s['s'][0]} -> {s['s'][-1]}")
    return SELECTED, Y0, Y1, series_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — continuous change over 44 years is the story
        - **Countries**: Mix of fast-aging (Japan, South Korea, Italy, Germany, France),
          mid-pace (China, Brazil), and slow-aging (India, Ethiopia) to show divergence
        - **Time range**: 1980-2023 captures industrialization era to present
        - **Color**: Warm for high values (aging), cool for low (young populations)
        - **Highlights**: Japan nearly quadrupled from 13% to 50%; Ethiopia stayed flat at ~5%
        """
    )
    return


@app.cell
def _(json, series_data):
    print(json.dumps(series_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
