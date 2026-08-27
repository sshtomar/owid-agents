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
        # Female Labor Force Participation by Region, 1990-2024 -- Methodology

        Trend lines showing the female labor force participation rate
        (% of female population ages 15-64) by world region, 1990-2024.
        The Arab World sits persistently below all other regions.
        South Asia shows a U-shaped trajectory. Europe & Central Asia trended up.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-ACTI-FE-ZS.json"
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
        'Arab World', 'North America', 'World'
    ]
    SHORT = {
        'Sub-Saharan Africa': 'Sub-Saharan Africa',
        'South Asia': 'South Asia',
        'East Asia & Pacific': 'East Asia & Pacific',
        'Europe & Central Asia': 'Europe & Central Asia',
        'Latin America & Caribbean': 'Latin America',
        'Arab World': 'Arab World',
        'North America': 'North America',
        'World': 'World'
    }

    all_data = {}
    for p in data:
        n = p['countryName']
        if n in REGION_NAMES and p['value'] is not None:
            if n not in all_data:
                all_data[n] = {}
            all_data[n][p['year']] = p['value']

    result = []
    for n, ydata in all_data.items():
        pts = [(y, round(v, 1)) for y, v in sorted(ydata.items()) if y >= 1990]
        result.append({'n': SHORT.get(n, n), 's': [v for y, v in pts], 'y0': 1990})
    result.sort(key=lambda x: -x['s'][-1])

    print("2024 values:")
    for r in result:
        print(f"  {r['n']}: {r['s'][-1]}% (1990: {r['s'][0]}%)")
    return result, all_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (annual 1990-2024)
        - **Story**: Arab World has remained persistently low (18-21%), the only region
          that has NOT meaningfully risen. South Asia dipped from 35% to 29% around 2015-2016
          before recovering. Europe & Central Asia rose from 59% to 66%.
          East Asia & Pacific slowly declined from 71% to 67%.
        - **Note COVID dip**: Visible as a drop in 2020 across all regions
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
