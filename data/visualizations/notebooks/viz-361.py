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
        # DPT Immunization Coverage — Methodology

        Trend lines for 10 countries showing coverage of DPT (diphtheria,
        pertussis, tetanus) vaccine from 1980-2024. Bangladesh's scale-up
        from <2% to 97% is the headline story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IDPT.json"
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
            'blended','demographic','transition','sub-saharan','high','low','upper','lower'}

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

    FEATURED = [
        ('Bangladesh','Bangladesh'), ('India','India'), ('Ethiopia','Ethiopia'),
        ('Chad','Chad'), ('Haiti','Haiti'), ('Afghanistan','Afghanistan'),
        ('Brazil','Brazil'), ('China','China'), ('Japan','Japan'), ('Germany','Germany'),
    ]

    series = []
    for feat, short in FEATURED:
        if feat in country_data:
            yd = country_data[feat]
            pts = sorted(yd.items())
            series.append({"n": short, "pts": [{"y": y, "v": round(v)} for y, v in pts]})
            early = yd.get(min(yd.keys()))
            late = yd.get(max(yd.keys()))
            print(f"  {short}: {early:.0f}% -> {late:.0f}%")
    return series,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows coverage trajectories over 44 years
        - **Country selection**: Dramatic risers (Bangladesh, India), laggards (Chad, Haiti), high achievers (Japan, Germany, China)
        - **Key insight**: Bangladesh went from 2% to 97% in under 25 years; Chad still at 68% after 40 years
        - **Smoothed data**: Some series use 5-year intervals for clarity
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
