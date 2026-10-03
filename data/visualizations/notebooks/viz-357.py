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
        # International Tourist Arrivals — Methodology

        Shows inbound tourist arrival counts for top destinations, 1995-2020,
        highlighting the COVID-19 collapse in 2020.
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
    SKIP_WORDS = {'world','income','states','dividend','europe','asia','africa','pacific',
            'america','middle','east','latin','caribbean','baltics','oecd','euro',
            'arab','south','north','western','eastern','central','developing','small',
            'island','region','average','union','members','hipc','heavily','indebted',
            'ida','ibrd','ifc','least','developed','classification','un','fragile',
            'blended','demographic','transition','sub-saharan'}

    def is_real_country(name):
        words = set(name.lower().replace(',','').replace('(','').replace(')','').replace('.','').replace('-','').split())
        return not any(w in SKIP_WORDS for w in words)

    country_data = {}
    for row in data:
        name = row['countryName']
        year = row['year']
        val = row['value']
        if is_real_country(name) and val is not None and val > 0:
            if name not in country_data:
                country_data[name] = {}
            country_data[name][year] = val

    FEATURED = ['France','China','Italy','Germany','Japan','Greece','Croatia','Australia']
    series = []
    for feat in FEATURED:
        if feat in country_data:
            yd = country_data[feat]
            pts = sorted([(y, v) for y, v in yd.items()], key=lambda x: x[0])
            short = feat.replace(' SAR, China','').replace(', Rep.','')
            series.append({"n": short, "pts": [{"y": y, "v": round(v/1e6, 2)} for y, v in pts]})

    print(f"Series count: {len(series)}")
    for s in series:
        last = s['pts'][-1]
        print(f"  {s['n']}: {s['pts'][0]['y']}-{last['y']}, peak={max(p['v'] for p in s['pts']):.1f}M, 2020={[p['v'] for p in s['pts'] if p['y']==2020]}")
    return series,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — multiple overlapping time series
        - **Country selection**: Top destinations available in dataset (France, China, Italy, etc.)
        - **Time range**: 1995-2020, ending at COVID collapse
        - **Highlights**: COVID drop in 2020 is the key story; China's rapid rise
        - **Colors**: Warm accent palette distinguishing high from lower destinations
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
