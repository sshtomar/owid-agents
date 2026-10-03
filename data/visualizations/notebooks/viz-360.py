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
        # Population Growth Rate — Methodology

        Trend lines for 8 countries spanning the full demographic spectrum,
        from high-growth Sub-Saharan Africa to declining Eastern Europe.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
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
        ('Chad', 'Chad'), ('Angola', 'Angola'),
        ('India', 'India'), ('Brazil', 'Brazil'),
        ('China', 'China'), ('Japan', 'Japan'),
        ('Korea, Rep.', 'S. Korea'), ('Bulgaria', 'Bulgaria'),
    ]

    series = []
    for feat, short in FEATURED:
        if feat in country_data:
            yd = country_data[feat]
            pts = sorted(yd.items())
            sampled = [(y, v) for y, v in pts if y % 2 == 1 or y in [1961, 2024]]
            series.append({"n": short, "pts": [{"y": y, "v": round(v, 2)} for y, v in sampled]})
            last = yd[max(yd.keys())]
            print(f"  {short}: latest={last:.2f}%")
    return series,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows long-run demographic transition
        - **Country selection**: High-growth (Chad, Angola), transitioning (India, Brazil), low/negative (China, Japan, S. Korea, Bulgaria)
        - **Time range**: 1961-2024 — covers full demographic transition era
        - **Zero line**: Dashed reference at 0% to show when countries enter population decline
        - **Key insight**: China entered negative growth in 2023; Chad accelerating upward
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
