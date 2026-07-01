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
        # Electricity Carbon Intensity 2000 vs. 2024 — Methodology

        Slope chart comparing carbon intensity of electricity generation (gCO2/kWh)
        between 2000 and 2024 for 20 major economies. Shows which countries have
        decarbonized their grids and which remain carbon-heavy.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--EMISSIONS-INTENSITY.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries_sel = {
        'FRA': 'France', 'NOR': 'Norway', 'BRA': 'Brazil', 'SWE': 'Sweden',
        'CAN': 'Canada', 'GBR': 'UK', 'DEU': 'Germany', 'USA': 'USA',
        'CHN': 'China', 'IND': 'India', 'ZAF': 'South Africa', 'POL': 'Poland',
        'AUS': 'Australia', 'JPN': 'Japan', 'KOR': 'South Korea', 'ESP': 'Spain',
        'ITA': 'Italy', 'TUR': 'Turkey', 'IDN': 'Indonesia', 'MEX': 'Mexico'
    }

    by_cc = {}
    for r in data:
        if r['country'] in countries_sel:
            by_cc.setdefault(r['country'], {})[r['year']] = r['value']

    slope = []
    for cc, name in countries_sel.items():
        a = by_cc.get(cc, {}).get(2000)
        b = by_cc.get(cc, {}).get(2024) or by_cc.get(cc, {}).get(2023)
        if a is not None and b is not None:
            slope.append({'n': name, 'a': round(a, 0), 'b': round(b, 0)})

    slope.sort(key=lambda x: -x['a'])
    print(f"Series: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']} -> {s['b']} gCO2/kWh ({s['b']-s['a']:+.0f})")
    return slope, by_cc, countries_sel


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (two time points) to highlight magnitude of change
        - **Color encoding**: Green for large reductions (>250 gCO2/kWh), amber for moderate,
          tan for small reductions, terra for increases
        - **Highlights**: UK cut intensity by 306 points (522→216), Spain by 325 (471→146),
          Germany by 236 (573→337). Indonesia and Japan moved in the wrong direction.
        - **Collision resolution**: Labels on both sides use resolveCollisions() with 13px min-gap
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
