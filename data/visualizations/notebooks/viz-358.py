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
        # Scientific and Technical Journal Articles — Methodology

        Shows annual publication counts for major scientific nations, 1996-2023.
        China's 27-fold increase is the headline finding.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-JRN-ARTC-SC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SKIP_WORDS = {'world','income','states','dividend','europe','asia','africa','pacific',
            'america','middle','east','latin','caribbean','baltics','oecd','euro',
            'arab','south','north','western','eastern','central','developing','small',
            'island','region','average','union','members','hipc','heavily','indebted',
            'ida','ibrd','ifc','least','developed','classification','un','fragile',
            'high','low','upper','lower'}

    def is_real_country(name):
        words = set(name.lower().replace(',','').replace('(','').replace(')','').replace('.','').replace('-','').split())
        return not any(w in SKIP_WORDS for w in words)

    country_data = {}
    for row in data:
        name = row['countryName']
        year = row['year']
        val = row['value']
        if is_real_country(name) and val is not None:
            if name not in country_data:
                country_data[name] = {}
            country_data[name][year] = val

    FEATURED = ['China','India','Germany','Japan','Italy','Korea, Rep.','Canada','France','Brazil','Iran, Islamic Rep.']
    NAMES = {'Korea, Rep.':'S. Korea','Iran, Islamic Rep.':'Iran'}

    series = []
    for feat in FEATURED:
        if feat in country_data:
            yd = country_data[feat]
            pts = sorted([(y, v) for y, v in yd.items()], key=lambda x: x[0])
            short = NAMES.get(feat, feat)
            series.append({"n": short, "pts": [{"y": y, "v": round(v)} for y, v in pts if v is not None]})

    for s in series:
        first = s['pts'][0]
        last = s['pts'][-1]
        mult = last['v'] / first['v']
        print(f"  {s['n']}: {first['v']:.0f} -> {last['v']:.0f} ({mult:.1f}x)")
    return series,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows exponential divergence over time
        - **Country selection**: Top 10 by 2023 publications (USA absent from dataset)
        - **Key insight**: China surpassed all others around 2016-2018
        - **Colors**: China in accent red to emphasize its outlier trajectory
        """
    )
    return


@app.cell
def _(json, series):
    import json as _json
    print(_json.dumps(series, separators=(',',':')))
    return


if __name__ == "__main__":
    app.run()
