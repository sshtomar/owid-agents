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
        # Old-Age Dependency Ratio -- Methodology

        Dataset: wb--SP-POP-DPND-OL (World Bank, SP.POP.DPND.OL)
        Shows the ratio of people 65+ to working-age population (15-64),
        expressed as a percentage. Sampled every 5 years from 1960 to 2024.
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
def _(data, json):
    target = {
        'JP': 'Japan', 'DE': 'Germany', 'IT': 'Italy', 'FR': 'France',
        'KR': 'Korea', 'CN': 'China', 'IN': 'India', 'BD': 'Bangladesh',
        'ET': 'Ethiopia', 'GH': 'Ghana', 'IR': 'Iran', 'IQ': 'Iraq',
        'BG': 'Bulgaria', 'HU': 'Hungary', 'CZ': 'Czechia', 'GR': 'Greece'
    }
    by_country = {}
    for r in data:
        if r['country'] in target and r['value'] is not None:
            code = r['country']
            if code not in by_country:
                by_country[code] = {'n': target[code], 's': {}}
            by_country[code]['s'][r['year']] = r['value']
    years = list(range(1960, 2021, 5)) + [2024]
    series = []
    for code, info in by_country.items():
        pts = info['s']
        vals = [round(pts[y], 1) if pts.get(y) else None for y in years]
        last = round(pts.get(2024, pts.get(2023, 0)), 1)
        series.append({"n": info['n'], "s": vals, "y0": 1960, "step": 5, "last": last})
    series.sort(key=lambda x: -x['last'])
    print(json.dumps(series))
    return series, years


if __name__ == "__main__":
    app.run()
