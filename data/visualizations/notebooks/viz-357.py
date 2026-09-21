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
        # UHC Service Coverage Index -- Methodology

        Documents the slope chart comparing UHC progress from early 2000s to 2020s.
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
    # Map ISO codes to country names for selected countries
    name_map = {
        'ETH': 'Ethiopia', 'NPL': 'Nepal', 'BGD': 'Bangladesh', 'UGA': 'Uganda',
        'RWA': 'Rwanda', 'NGA': 'Nigeria', 'PAK': 'Pakistan', 'IND': 'India',
        'VNM': 'Vietnam', 'KHM': 'Cambodia', 'GHA': 'Ghana', 'KEN': 'Kenya',
        'TZA': 'Tanzania', 'CHN': 'China', 'THA': 'Thailand', 'TUR': 'Turkey',
        'MEX': 'Mexico', 'BRA': 'Brazil', 'COL': 'Colombia', 'IRN': 'Iran',
        'ZAF': 'South Africa', 'PHL': 'Philippines', 'MAR': 'Morocco',
        'GBR': 'United Kingdom', 'JPN': 'Japan', 'CAF': 'Central African Rep.',
    }
    by_country = {}
    for pt in data:
        cc = pt['country']
        if cc in name_map and pt['value'] is not None:
            if cc not in by_country:
                by_country[cc] = []
            by_country[cc].append((pt['year'], pt['value']))
    print(f"Filtered to {len(by_country)} target countries")
    return by_country, name_map


@app.cell
def _(by_country, json, name_map):
    # Build slope chart data: earliest (~2000-2005) vs latest (~2018-2023)
    slope_data = []
    for cc, pts in by_country.items():
        pts_sorted = sorted(pts)
        early = [(y, v) for y, v in pts_sorted if y <= 2005]
        late = [(y, v) for y, v in pts_sorted if y >= 2018]
        if early and late:
            early_yr, early_val = early[0]
            late_yr, late_val = late[-1]
            change = round(late_val - early_val, 1)
            slope_data.append({
                'n': name_map[cc],
                'a': round(early_val, 1),
                'b': round(late_val, 1),
                'ya': early_yr,
                'yb': late_yr,
                'ch': change
            })

    slope_data.sort(key=lambda x: -x['ch'])
    print(f"Slope pairs: {len(slope_data)}")
    for s in slope_data:
        print(f"  {s['n']}: {s['a']} ({s['ya']}) -> {s['b']} ({s['yb']}) +{s['ch']}")
    print(json.dumps(slope_data, separators=(',', ':')))
    return (slope_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for showing change between two time points across many countries
        - **Country selection**: 21 countries spanning all income groups, with strong early+late data coverage
        - **Color**: Encodes magnitude of improvement (deepest change = most saturated orange-red)
        - **Story**: Low-income countries (Nepal, Rwanda) made dramatic gains from very low baselines;
          China's surge reflects universal coverage push; wealthy nations improved modestly from already high scores
        """
    )
    return


if __name__ == "__main__":
    app.run()
