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
        # Lifetime Risk of Maternal Death — Methodology

        Documents the data pipeline behind viz-512.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MMR-RISK-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_country = {}
    for row in data:
        c = row['countryName']
        if row['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][row['year']] = row['value']
    print(f"Countries loaded: {len(by_country)}")
    return (by_country,)


@app.cell
def _(by_country):
    selected = [
        'Chad', 'Congo, Dem. Rep.', 'Angola', 'Guinea', 'Afghanistan',
        'Cameroon', 'Kenya', 'India', 'Bangladesh', 'Bolivia',
        'Indonesia', 'Brazil', 'China',
        'Iceland', 'France', 'Germany', 'Japan'
    ]
    result = []
    for c in selected:
        if c not in by_country:
            continue
        years = by_country[c]
        y1990 = years.get(1990)
        y2023 = years.get(2023) or years.get(2022)
        if y1990 and y2023:
            display = c.replace('Congo, Dem. Rep.', 'DR Congo')
            # Express as per 1,000 women for readability
            result.append({'n': display, 'a': round(y1990 * 1000, 2), 'b': round(y2023 * 1000, 2)})
    result.sort(key=lambda x: -x['a'])
    print(f"Countries: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['a']} -> {r['b']} per 1,000")
    return result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart with log scale — 1990 vs 2023
        - **Unit**: per 1,000 women (lifetime risk), multiplied from raw percentage
        - **Scale**: Logarithmic Y-axis because values span 3 orders of magnitude (0.03 to 107)
        - **Story**: Chad barely improved; Bangladesh dropped 16x; Japan is 380x safer than Chad
        - **Country selection**: High-risk (Sub-Saharan Africa, South Asia) through low-risk (Western Europe)
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
