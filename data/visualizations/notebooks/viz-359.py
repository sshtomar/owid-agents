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
        # Researchers in R&D -- Methodology

        Trend lines for 8 countries showing researchers per million people, 1996-2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-SCIE-RD-P6.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    targets = {
        'Korea, Rep.': 'South Korea', 'Japan': 'Japan', 'Germany': 'Germany',
        'France': 'France', 'China': 'China', 'Canada': 'Canada',
        'Finland': 'Finland', 'India': 'India',
    }
    by_country = {}
    for pt in data:
        cn = pt.get('countryName', '')
        if cn in targets:
            yr = pt['year']
            val = pt.get('value')
            if val is not None:
                label = targets[cn]
                if label not in by_country:
                    by_country[label] = {}
                by_country[label][yr] = round(val, 0)

    chart_data = []
    for label, vals in by_country.items():
        pts = sorted([{'y': y, 'v': int(v)} for y, v in vals.items()], key=lambda x: x['y'])
        chart_data.append({'n': label, 'pts': pts})
    chart_data.sort(key=lambda x: -x['pts'][-1]['v'])

    for c in chart_data:
        latest = c['pts'][-1]
        print(f"  {c['n']}: {latest['v']} ({latest['y']})")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectories, not just snapshots
        - **Country selection**: Mix of high performers (South Korea, Finland) and large economies (Germany, France, Japan, Canada) plus China's rise and India's low base
        - **Story**: South Korea's fourfold increase (2186 to 9472) is exceptional; China grew from 447 to 2107 showing rapid catch-up; India remains far behind at 259 per million
        """
    )
    return


if __name__ == "__main__":
    app.run()
