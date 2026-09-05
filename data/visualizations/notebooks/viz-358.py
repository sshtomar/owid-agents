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
        # Energy Intensity of GDP, 2000 vs 2021-2022 -- Methodology

        Slope chart comparing megajoules of primary energy consumed per $2021 PPP GDP.
        Shows the broad trend of decoupling economic output from energy consumption.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-EGY-PRIM-PP-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    selected = ['Bhutan', 'Azerbaijan', 'Iceland', 'China', 'Bulgaria', 'Canada',
                'Estonia', 'Korea, Rep.', 'India', 'Czechia', 'Australia',
                'Hungary', 'Japan', 'Chile', 'France', 'Croatia', 'Germany', 'Ireland']

    by_country = defaultdict(dict)
    for p in data:
        if p['countryName'] in selected and p['value'] is not None:
            by_country[p['countryName']][p['year']] = p['value']

    result = []
    for c in selected:
        yrs = by_country.get(c, {})
        v2000 = yrs.get(2000)
        recent = max([(yr, v) for yr, v in yrs.items() if yr >= 2018], key=lambda x: x[0], default=(None, None))
        if v2000 and recent[1]:
            display = c.replace('Korea, Rep.', 'South Korea')
            result.append({'n': display, 'a': round(v2000, 2), 'b': round(recent[1], 2)})

    result.sort(key=lambda x: -x['a'])
    for r in result:
        pct = (r['b'] - r['a']) / r['a'] * 100
        print(f"{r['n']}: {r['a']} -> {r['b']} ({pct:+.1f}%)")
    return result, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2021-22) to highlight change magnitude
        - **Color**: Green for >60% reduction, through amber/terra to orange for increases
        - **Story**: Ireland dropped from 3.12 to 0.97 MJ/$GDP (-69%), a dramatic shift
          driven by the growth of low-energy service sectors. Iceland barely changed
          (high geothermal use). China fell 42% despite massive industrialization.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
