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
        # Renewable Share of Total Final Energy, 2000 vs. 2020 -- Methodology

        Slope chart showing how the renewable share of total final energy consumption
        changed between 2000 and 2020. This metric is broader than electricity-only
        renewable stats: it includes heat and transport as well.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-FEC-RNEW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected_names = {
        'Denmark', 'Germany', 'Ireland', 'Italy', 'Finland', 'Estonia', 'Iceland', 'Brazil',
        'Bangladesh', 'Indonesia', 'Ghana', 'Cambodia', 'Afghanistan', 'Gabon', 'India', 'China',
        'Chile', 'Colombia', 'Albania', 'Bolivia'
    }

    by_country = {}
    for pt in data:
        c = pt['countryName']
        if c not in selected_names or pt['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][pt['year']] = pt['value']

    slope = []
    for c in selected_names:
        a = by_country.get(c, {}).get(2000)
        b = by_country.get(c, {}).get(2020)
        if a is not None and b is not None:
            slope.append({'n': c, 'a': round(a, 1), 'b': round(b, 1)})
            print(f"{c}: {a:.1f}% -> {b:.1f}% ({b-a:+.1f}pp)")

    slope.sort(key=lambda x: x['b'], reverse=True)
    return slope, by_country, selected_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2020)
        - **Color**: Green for increases, red/orange for decreases
        - **Story**: European nations rapidly scaled renewables; many developing nations
          saw their renewable share *fall* as fossil-fuel power expanded to meet growth.
          Iceland and Gabon were already high and climbed further.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
