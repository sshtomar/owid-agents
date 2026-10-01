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
        # Energy Intensity, 2000-2022 -- Methodology

        Trend lines showing how major economies reduced the energy required to
        produce each unit of GDP (MJ per 2021 PPP dollar). Falling lines mean
        the economy is becoming more energy-efficient.
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
    target = {'China', 'India', 'Germany', 'Japan', 'France',
              'Australia', 'Brazil', 'Canada', 'Indonesia', 'Kazakhstan'}

    cdata = {}
    for row in data:
        if row['countryName'] not in target or row['value'] is None:
            continue
        c = row['countryName']
        if c not in cdata:
            cdata[c] = {}
        cdata[c][row['year']] = round(row['value'], 3)

    start_yr, end_yr = 2000, 2022
    result = []
    for c in sorted(cdata.keys()):
        if start_yr not in cdata[c]:
            continue
        s = []
        for y in range(start_yr, end_yr + 1):
            if y in cdata[c]:
                s.append(round(cdata[c][y], 3))
            elif s:
                s.append(s[-1])
        while s and s[-1] is None:
            s.pop()
        result.append({'n': c, 's': s, 'y0': start_yr})

    result.sort(key=lambda x: x['s'][0], reverse=True)
    print(f"Series: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['s'][0]} -> {r['s'][-1]:.3f}")
    return result, cdata, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines, 2000-2022 (annual)
        - **Story**: China started as the most energy-intensive and cut intensity
          nearly in half. Kazakhstan remains high. Ireland, Germany, France lead
          in efficiency. Brazil and Indonesia improved moderately.
        - **Color**: Warm ramp by 2022 energy intensity level (high = red/amber,
          low = cool)
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
