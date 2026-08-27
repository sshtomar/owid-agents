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
        # Urban Population Growth Rate by Region, 1990-2024 -- Methodology

        Trend lines showing the annual urban population growth rate (%)
        by world region from 1990 to 2024. Sub-Saharan Africa leads at ~3.6%
        annually; Europe & Central Asia and North America have slowed to under 1%.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-URB-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    REGION_NAMES = [
        'Sub-Saharan Africa', 'South Asia', 'East Asia & Pacific',
        'Europe & Central Asia', 'Latin America & Caribbean',
        'North America', 'World'
    ]

    all_data = {}
    for p in data:
        n = p['countryName']
        if n in REGION_NAMES and p['value'] is not None:
            if n not in all_data:
                all_data[n] = {}
            all_data[n][p['year']] = p['value']

    result = []
    for n, ydata in all_data.items():
        pts = [(y, round(v, 2)) for y, v in sorted(ydata.items()) if y >= 1990]
        result.append({'n': n, 's': [v for y, v in pts], 'y0': 1990})
    result.sort(key=lambda x: -x['s'][-1])

    print("2024 urban growth rates:")
    for r in result:
        print(f"  {r['n']}: {r['s'][-1]}% (1990: {r['s'][0]}%)")
    return result, all_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (annual 1990-2024)
        - **Story**: Sub-Saharan Africa continues rapid urbanization (~3.6%/yr).
          East Asia & Pacific has been volatile due to China's reclassification of
          rural areas. Latin America has slowed dramatically (4.2% -> ~1%).
          Europe is nearly flat at 0-1%.
        - **Color**: Warm for fast-growing, cool for slow
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
