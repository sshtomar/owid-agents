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
        # Rise of Non-Communicable Disease Deaths by Region, 2000-2021 -- Methodology

        Trend lines showing the share of total deaths caused by non-communicable
        diseases (NCDs: heart disease, cancer, diabetes, etc.) by world region.
        Data points exist for 2000, 2010, 2015, 2019, 2020, and 2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DTH-NCOM-ZS.json"
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
        'Middle East, North Africa, Afghanistan & Pakistan',
        'North America', 'World'
    ]
    SHORT = {
        'Sub-Saharan Africa': 'Sub-Saharan Africa',
        'South Asia': 'South Asia',
        'East Asia & Pacific': 'East Asia & Pacific',
        'Europe & Central Asia': 'Europe & Central Asia',
        'Latin America & Caribbean': 'Latin America & Caribbean',
        'Middle East, North Africa, Afghanistan & Pakistan': 'Mid. East & N. Africa',
        'North America': 'North America',
        'World': 'World'
    }

    regions = {}
    for p in data:
        n = p['countryName']
        if n in REGION_NAMES and p['value'] is not None:
            if n not in regions:
                regions[n] = {}
            regions[n][p['year']] = p['value']

    result = []
    for n, ydata in regions.items():
        pts_sorted = sorted(ydata.items())
        result.append({'n': SHORT.get(n, n), 'pts': [{'y': y, 'v': round(v, 1)} for y, v in pts_sorted]})
    result.sort(key=lambda x: -x['pts'][-1]['v'])

    print("Regions and their 2019 peak vs 2021 value:")
    for r in result:
        pts = {p['y']: p['v'] for p in r['pts']}
        print(f"  {r['n']}: 2000={pts.get(2000)}%, 2019={pts.get(2019)}%, 2021={pts.get(2021)}%")
    return result, regions


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (connected dots at irregular intervals)
        - **Story**: All regions trended upward 2000-2019 as infectious diseases declined.
          The 2020-2021 dip reflects COVID-19 reclassifying many deaths as communicable.
          Sub-Saharan Africa remains far below global average (~35% vs 63%).
        - **Color**: 8 distinct colors, World highlighted in darker tone
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
