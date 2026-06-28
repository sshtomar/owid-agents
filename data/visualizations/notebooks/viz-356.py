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
        # Safe Drinking Water Progress, 2000-2022 -- Methodology

        Slope chart comparing access to safely managed drinking water services
        (% of population) in 2000 versus 2022. Highlights where rapid progress
        was made and where coverage stagnated or declined.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-H2O-SMDW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    selected = {
        'ET': 'Ethiopia', 'TD': 'Chad', 'CF': 'C. Afr. Rep.', 'CD': 'Congo DR',
        'GH': 'Ghana', 'AF': 'Afghanistan', 'KH': 'Cambodia', 'GM': 'Gambia',
        'CG': 'Congo', 'BT': 'Bhutan', 'IN': 'India', 'AL': 'Albania',
        'HN': 'Honduras', 'JO': 'Jordan', 'KZ': 'Kazakhstan', 'BD': 'Bangladesh',
    }

    by_country = defaultdict(dict)
    for x in data:
        if x['country'] in selected and x['value'] is not None:
            by_country[x['country']][x['year']] = x['value']

    slope = []
    for cc, name in selected.items():
        yrs = by_country.get(cc, {})
        a = yrs.get(2000)
        b = yrs.get(2022) or yrs.get(2021)
        if a is not None and b is not None:
            slope.append({'n': name, 'a': round(a, 1), 'b': round(b, 1)})

    slope.sort(key=lambda x: x['a'])
    print(f"Series: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% ({s['b']-s['a']:+.1f}pp)")
    return slope, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2022) to highlight the magnitude of change
        - **Color**: Green for big gains (>20pp), amber for moderate, red for near-stagnant or declining
        - **Story**: India jumped from 38% to 73%, Bhutan from 28% to 68%, Jordan from 56% to 85%.
          Central African Republic declined from 8.5% to 6.1%. Chad barely moved from 5.5% to 6.2%.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
