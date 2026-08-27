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
        # Cause of Death by Injury, 2000 vs 2021 -- Methodology

        Slope chart comparing the share of total deaths attributable to injuries
        (road traffic, violence, drowning, falls, etc.) in 2000 vs 2021 for the
        25 countries with the highest injury death share in 2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DTH-INJR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    EXCLUDE_TERMS = [
        'income','region','IDA','IBRD','World','dividend','OECD','Zone',
        'Europa','union','Union','countries','classification',
        'Eastern and Southern','Western and Central','North Africa',
        'Central Asia','Pacific','Latin America','Caribbean','Sub-Saharan',
        'Arab ','South Asia','East Asia','Europe & Central','North America',
        'Middle East','African Union'
    ]

    by_country = {}
    for p in data:
        n = p['countryName']
        if any(ex.lower() in n.lower() for ex in EXCLUDE_TERMS):
            continue
        if p['value'] is not None:
            if n not in by_country:
                by_country[n] = {}
            by_country[n][p['year']] = p['value']

    both = []
    for n, ydata in by_country.items():
        if 2000 in ydata and 2021 in ydata:
            both.append({'n': n, 'a': round(ydata[2000], 2), 'b': round(ydata[2021], 2)})

    both.sort(key=lambda x: -x['b'])
    slope_data = both[:25]
    print(f"Countries with both years: {len(both)}")
    print(f"Selected top 25 by 2021 injury death %")
    for s in slope_data:
        chg = s['b'] - s['a']
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({chg:+.1f}pp)")
    return slope_data, by_country, both


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2021) to show trajectory of injury mortality
        - **Color**: Red (#EA5E33) = increased, green (#3D7A5A / #A6C4A2) = decreased
        - **Story**: Afghanistan surged from 9.5% to 23.2% (conflict-driven).
          Colombia fell from 26.9% to 9.7% as the peace process took hold.
          Sub-Saharan African countries like Kenya, Burkina Faso, and Cote d'Ivoire saw rises.
        """
    )
    return


@app.cell
def _(json, slope_data):
    print(json.dumps(slope_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
