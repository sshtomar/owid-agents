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
        # Population Growth Rate by World Region — Methodology

        Sparkline grid showing annual population growth rate trends (1961-2024)
        for major world regions. Shows diverging trajectories across the globe.
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
    regions = [
        'Sub-Saharan Africa', 'Middle East & North Africa', 'South Asia',
        'Latin America & Caribbean', 'East Asia & Pacific',
        'Europe & Central Asia', 'North America', 'World'
    ]
    by_region = {}
    for x in data:
        if x['countryName'] in regions and x['value'] is not None:
            if x['countryName'] not in by_region:
                by_region[x['countryName']] = {}
            by_region[x['countryName']][x['year']] = x['value']

    result = []
    for r in regions:
        if r in by_region:
            yv = by_region[r]
            years = sorted(yv.keys())
            series = [round(yv[y], 2) for y in years]
            result.append({"n": r, "s": series, "y0": years[0], "step": 1})
    print("Regions extracted:", [x['n'] for x in result])
    return by_region, regions, result


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
