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
        # Intentional Homicides: 1990 vs 2022 -- Methodology

        Slope chart comparing intentional homicide rates (per 100,000 people)
        around 1990 and 2022. Shows Colombia's dramatic decline alongside
        rising rates in several Caribbean and Central American nations.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['Colombia', 'Jamaica', 'Ecuador', 'Honduras', 'Guatemala',
                'Brazil', 'Costa Rica', 'India', 'Kazakhstan', 'Australia',
                'Germany', 'Italy', 'Japan']

    cdata = {}
    for row in data:
        if row['countryName'] not in selected or row['value'] is None:
            continue
        c = row['countryName']
        if c not in cdata:
            cdata[c] = {}
        cdata[c][row['year']] = round(row['value'], 2)

    slope = []
    for c in selected:
        if c not in cdata:
            continue
        yrs = cdata[c]
        a = next((yrs[y] for y in [1990, 1991, 1992] if y in yrs), None)
        b = next((yrs[y] for y in [2023, 2022, 2021, 2020] if y in yrs), None)
        if a is not None and b is not None:
            slope.append({'n': c, 'a': a, 'b': b})

    slope.sort(key=lambda x: x['a'], reverse=True)
    print(f"Series: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['b']-s['a']:+.2f})")
    return slope, cdata, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (1990 vs ~2022) to show direction of change
        - **Color**: Green for declining rates (improvement), red/amber for rising
        - **Story**: Colombia fell from 75 to 25 per 100k — a remarkable drop.
          Ecuador surged from 8.5 to 45.7. Jamaica and Honduras also worsened
          substantially. Italy and Australia are near 1 per 100k.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
