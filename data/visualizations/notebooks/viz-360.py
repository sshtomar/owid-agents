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
        # Deaths from Non-Communicable Diseases: 2000 vs. 2019 -- Methodology

        Slope chart showing the share of deaths attributed to non-communicable diseases
        (NCDs: heart disease, cancer, diabetes, etc.) in 2000 versus 2019. The global
        epidemiological transition in one view.
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
    selected = {
        'Bulgaria', 'Finland', 'Germany', 'Ireland', 'China', 'Brazil', 'India', 'Indonesia',
        'Bangladesh', 'Kenya', 'Ethiopia', 'Ghana', 'Burkina Faso', 'Chad', 'Iraq',
        'Egypt, Arab Rep.', 'Colombia', 'Bolivia', 'Albania'
    }

    by_country = {}
    for pt in data:
        c = pt['countryName']
        if c not in selected or pt['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][pt['year']] = pt['value']

    slope = []
    for c in selected:
        a = by_country.get(c, {}).get(2000)
        b = by_country.get(c, {}).get(2019)
        if a is not None and b is not None:
            name = c.replace('Egypt, Arab Rep.', 'Egypt')
            slope.append({'n': name, 'a': round(a, 1), 'b': round(b, 1)})
            print(f"{name}: {a:.1f}% -> {b:.1f}% ({b-a:+.1f}pp)")

    slope.sort(key=lambda x: x['b'], reverse=True)
    return slope, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2019)
        - **Color**: Green for high NCD share (advanced transition), orange/red for low share
        - **Story**: European countries at 90%+ NCD share; rapid transitions in Bangladesh,
          India, and Indonesia; Chad and Burkina Faso still below 40% (communicable disease burden)
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
