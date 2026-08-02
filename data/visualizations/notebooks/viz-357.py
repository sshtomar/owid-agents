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
        # International Tourist Arrivals, 1995–2020 -- Methodology

        Trend line chart showing inbound tourist arrivals for 7 selected countries
        from 1995 to 2020. COVID-19 caused the largest single-year collapse in
        recorded tourism history.
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
    SKIP_WORDS = ['World', 'income', 'members', 'dividend', ' Asia', 'Africa',
                   'Europe', 'America', 'Carib', 'Middle East', 'Pacific',
                   'IBRD', 'IDA', 'OECD', 'Union', 'area', 'states', 'countries',
                   'Least developed', 'HIPC', 'Heavily', 'small states', 'North America']

    def is_country(code, name):
        if code[0].isdigit(): return False
        for w in SKIP_WORDS:
            if w.lower() in name.lower(): return False
        return True

    SELECTED = {'China', 'Italy', 'Croatia', 'Hong Kong SAR, China', 'Germany', 'Japan', 'Korea, Rep.'}

    by_country = {}
    for row in data:
        name = row['countryName']
        if name in SELECTED and row['value'] is not None:
            y = row['year']
            if name not in by_country:
                by_country[name] = []
            by_country[name].append({"y": y, "v": round(row['value'] / 1e6, 2)})

    result = []
    for name, pts in by_country.items():
        pts_sorted = sorted(pts, key=lambda p: p['y'])
        result.append({"n": name, "pts": pts_sorted})

    result.sort(key=lambda x: -x['pts'][-1]['v'])

    for s in result:
        pts = s['pts']
        print(f"{s['n']}: {pts[0]['y']}-{pts[-1]['y']}, "
              f"2019={next((p['v'] for p in pts if p['y']==2019), 'N/A'):.1f}M, "
              f"2020={next((p['v'] for p in pts if p['y']==2020), 'N/A')}")
    return result, by_country, SELECTED


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how each country's arrivals evolved over 25 years
        - **Country selection**: 7 countries across Asia and Europe with full 1995–2020 data
        - **Key insight**: Hong Kong crashed 94% (65M→4M), Japan 87% (32M→4M), Korea 86% (18M→3M)
        - **COVID band**: vertical dashed line at 2020 marks the collapse
        - **Y-axis**: capped at 170M (China reaches 163M at peak); Croatia/Korea/Japan visible on lower range
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
