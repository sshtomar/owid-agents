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
        # Poverty at $3/day: Regional Trajectories Since 1981 -- Methodology

        Trend lines showing the share of population living below $3.00/day
        (2021 PPP) across world regions and selected high-poverty countries.
        East Asia's dramatic decline contrasts with near-stagnation in
        Sub-Saharan Africa.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-POV-DDAY.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {
        'East Asia & Pacific': 'East Asia & Pacific',
        'South Asia': 'South Asia',
        'Sub-Saharan Africa': 'Sub-Saharan Africa',
        'Latin America & Caribbean': 'Latin America',
        'China': 'China',
        'Indonesia': 'Indonesia',
        'Bangladesh': 'Bangladesh',
    }

    cdata = {}
    for row in data:
        if row['countryName'] not in target or row['value'] is None:
            continue
        c = target[row['countryName']]
        if c not in cdata:
            cdata[c] = {}
        cdata[c][row['year']] = round(row['value'], 1)

    # Build annual series 1981-2024 (sparse for countries, fill forward)
    result = []
    for c in sorted(cdata.keys()):
        pts = {}
        for y, v in cdata[c].items():
            pts[y] = v
        # Build sparse list using pts dict; we'll include only years with data
        year_vals = sorted(pts.items())
        result.append({'n': c, 'pts': year_vals})

    result.sort(key=lambda x: x['pts'][0][1], reverse=True)
    print(f"Series: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['pts'][0]} -> {r['pts'][-1]}")
    return result, cdata, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with sparse explicit year-value pairs
        - **Story**: East Asia & Pacific plunged from 77% in 1981 to 2% in 2024
          — the most dramatic poverty reduction in history. Sub-Saharan Africa
          barely moved (61% → 45%). South Asia tracked East Asia at a lag.
          China single-handedly drove much of the global poverty reduction.
        - **Color**: Warm ramp by 2022/latest poverty share (high = warm)
        """
    )
    return


@app.cell
def _(json, result):
    # Export as explicit year-value pairs for HTML
    export = [{'n': r['n'], 'pts': r['pts']} for r in result]
    print(json.dumps(export, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
