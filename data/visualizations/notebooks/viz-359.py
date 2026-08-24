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
        # Poverty Headcount at $3.00/Day: Country Trajectories -- Methodology

        Sparkline grid showing the share of the population living below $3/day (2021 PPP).
        Highlights the dramatic poverty reduction in East and South Asia versus persistent
        high poverty in Sub-Saharan Africa.
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
    selected = {'China', 'India', 'Bangladesh', 'Brazil', 'Ethiopia', 'Kenya',
                'Ghana', 'Congo, Dem. Rep.', 'Bolivia', 'Indonesia'}

    by_country = {}
    for pt in data:
        c = pt['countryName']
        if c not in selected or pt['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][pt['year']] = pt['value']

    chart_data = []
    for c in selected:
        vals = by_country.get(c, {})
        pts = sorted([(y, v) for y, v in vals.items() if y >= 2000], key=lambda x: x[0])
        if not pts:
            continue
        name = c.replace('Congo, Dem. Rep.', 'D.R. Congo')
        first_v = pts[0][1]
        last_v = pts[-1][1]
        chart_data.append({
            'n': name,
            'pts': [{'y': y, 'v': round(v, 1)} for y, v in pts],
            'first': round(first_v, 1),
            'last': round(last_v, 1)
        })
        print(f"{name}: {pts[0][0]}:{first_v:.1f}% -> {pts[-1][0]}:{last_v:.1f}%")

    # Sort by change (biggest drop first)
    chart_data.sort(key=lambda d: d['last'] - d['first'])
    return chart_data, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid (one per country)
        - **Sorting**: Biggest absolute decline first (most progress at top-left)
        - **Story**: China eliminated $3/day poverty almost entirely; India and Bangladesh
          made major gains. D.R. Congo remains at 85%. Kenya stagnated and even worsened.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
