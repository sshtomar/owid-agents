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
        # Adjusted Net Savings Trend Lines — Methodology

        Trend line chart showing adjusted net savings (% of GNI) across 10 countries, 1995–2021.
        Adjusted net savings deducts depletion of forests, minerals, energy, and particulate emission damage.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-ADJ-SVNG-GN-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    focus = ['Bangladesh', 'India', 'China', 'Germany', 'Indonesia', 'Brazil', 'Guinea', 'Chile', 'Bolivia', 'Australia']
    result = {}
    for p in data:
        n = p['countryName']
        if n in focus and p.get('value') is not None and p['year'] >= 1995 and (p['year'] % 2 == 1 or p['year'] in [1995, 2021]):
            if n not in result:
                result[n] = {'n': n, 'pts': []}
            if p['year'] not in {pt['y'] for pt in result[n]['pts']}:
                result[n]['pts'].append({'y': p['year'], 'v': round(p['value'], 1)})
    final = [{'n': result[n]['n'], 'pts': sorted(result[n]['pts'], key=lambda x: x['y'])}
             for n in focus if n in result]
    print(f"Countries: {len(final)}")
    for s in final:
        pts = s['pts']
        print(f"{s['n']}: {pts[0]['v']}% (1995) -> {pts[-1]['v']}% (2021)")
    return final, focus, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows whether countries are building or depleting genuine wealth over time
        - **Country selection**: Bangladesh (rising star), China/India (large developing), Germany (benchmark rich country), Indonesia/Brazil/Bolivia/Chile (resource-dependent), Guinea (chronic negative), Australia (mining-intensive)
        - **Zero line**: Critical reference — negative means consuming natural capital faster than saving
        - **Color**: Green for positive trajectory, red for negative/declining
        - **Key insight**: Bangladesh's rise to 32% is driven by human capital investment and low resource depletion
        """
    )
    return


@app.cell
def _(final, json):
    print(json.dumps(final, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
