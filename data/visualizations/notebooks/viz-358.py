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
        # Manufacturing Value Added as % of GDP, 2000-2024 -- Methodology

        Trend lines for 9 countries showing diverging trajectories: deindustrialization
        in rich Western economies vs. rising manufacturing share in developing Asia.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-MANF-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    by_c = defaultdict(dict)
    for x in data:
        if x['value'] is not None:
            by_c[x['countryName']][x['year']] = x['value']

    story = {
        'Korea, Rep.': 'South Korea',
        'China': 'China',
        'Germany': 'Germany',
        'Japan': 'Japan',
        'France': 'France',
        'Bangladesh': 'Bangladesh',
        'India': 'India',
        'Indonesia': 'Indonesia',
        'Australia': 'Australia',
    }

    series = []
    for orig, label in story.items():
        if orig in by_c:
            pts = sorted([(y, round(v,1)) for y,v in by_c[orig].items() if 2000 <= y <= 2024])
            series.append({'n': label, 'pts': [{'y': y, 'v': v} for y,v in pts]})

    for s in series:
        first = s['pts'][0]
        last = s['pts'][-1]
        print(f"{s['n']}: {first['y']}={first['v']}% -> {last['y']}={last['v']}%")
    return by_c, series, story


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with hover isolation
        - **Countries**: 9 representing three groups:
          1. Deindustrializing rich nations (Germany, Japan, France, Australia)
          2. Industrializing developing nations (Bangladesh, Indonesia rising, then stalling)
          3. East Asian anchor (South Korea: stable ~27%; China: peak ~32% declining)
        - **Story**: France fell from 14% to under 10%. Australia from 11% to 5%.
          Bangladesh rose steadily from 14% to 22%. South Korea held firm at 26-29%.
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
