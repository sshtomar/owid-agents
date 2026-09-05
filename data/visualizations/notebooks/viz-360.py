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
        # Pre-Primary School Enrollment, 2000 vs 2020-2021 -- Methodology

        Slope chart comparing gross enrollment in pre-primary education across countries.
        Shows remarkable expansion of early childhood education in developing countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRE-ENRR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    selected = ['Ghana', 'Georgia', 'Costa Rica', 'China', 'Finland', 'Kazakhstan',
                'Iran, Islamic Rep.', 'Kenya', 'Indonesia', 'Bhutan', 'Azerbaijan',
                'Bangladesh', 'Cambodia', 'Ethiopia']

    by_country = defaultdict(dict)
    for p in data:
        if p['countryName'] in selected and p['value'] is not None:
            by_country[p['countryName']][p['year']] = p['value']

    result = []
    for c in selected:
        yrs = by_country.get(c, {})
        v2000 = yrs.get(2000)
        recent_entries = [(yr, v) for yr, v in yrs.items() if yr >= 2018]
        if v2000 is not None and recent_entries:
            yr, vr = max(recent_entries, key=lambda x: x[0])
            display = c.replace('Iran, Islamic Rep.', 'Iran')
            result.append({'n': display, 'a': round(v2000, 1), 'b': round(vr, 1)})

    result.sort(key=lambda x: -x['b'])
    for r in result:
        gain = r['b'] - r['a']
        print(f"{r['n']}: {r['a']}% -> {r['b']}% (+{gain:.1f}pp)")
    return result, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2020-21) to show absolute change
        - **Color**: Green for >50pp gain, through amber to terra for moderate gains
        - **Story**: Ghana rose from 60% to 116% (above 100% because older children attend).
          Bhutan jumped from just 1.1% to 51.9% — nearly 50-fold in two decades.
          Ethiopia from 1.6% to 30.1%. Iran from 18.5% to 72.5%.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
