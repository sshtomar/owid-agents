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
        # Crude Death Rate -- Methodology

        Dataset: wb--SP-DYN-CDRT-IN (World Bank, SP.DYN.CDRT.IN)
        Shows crude death rate (deaths per 1,000 people) for 16 selected countries
        from 1960 to 2023 sampled every 5 years.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-CDRT-IN.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {
        'JP': 'Japan', 'DE': 'Germany', 'IT': 'Italy', 'FR': 'France',
        'KR': 'Korea', 'CN': 'China', 'IN': 'India', 'BD': 'Bangladesh',
        'BG': 'Bulgaria', 'BY': 'Belarus', 'ET': 'Ethiopia', 'ID': 'Indonesia',
        'IR': 'Iran', 'IQ': 'Iraq', 'GH': 'Ghana', 'CG': 'Congo'
    }
    by_country = {}
    for r in data:
        if r['country'] in target and r['value'] is not None:
            code = r['country']
            if code not in by_country:
                by_country[code] = {'n': target[code], 's': {}}
            by_country[code]['s'][r['year']] = r['value']
    print(f"Countries extracted: {len(by_country)}")
    return by_country, target


@app.cell
def _(by_country, json):
    years = list(range(1960, 2021, 5)) + [2023]
    series = []
    for code, info in by_country.items():
        pts = info['s']
        vals = [round(pts[y], 2) if pts.get(y) else None for y in years]
        last = round(pts.get(2023, pts.get(2022, 0)), 2)
        series.append({"n": info['n'], "s": vals, "y0": 1960, "step": 5, "last": last})
    series.sort(key=lambda x: -x['last'])
    print(f"Series: {len(series)} countries")
    print(f"Year range: {years[0]}-{years[-1]}, {len(years)} points")
    print(json.dumps(series))
    return series, years


if __name__ == "__main__":
    app.run()
