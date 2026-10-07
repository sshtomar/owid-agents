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
        # Hydroelectric Power's Grip and Release — Methodology

        Documents the data pipeline for viz-362: hydro electricity as % of total
        generation, 2000 vs. most recent year.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-HYRO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    print(f"Countries: {len(set(d['countryName'] for d in data))}, Years: {min(d['year'] for d in data)}-{max(d['year'] for d in data)}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    SKIP = ['income','World','states','dividend','Pacific','Atlantic','Caribbean',
            'Middle East','Arab','Euro area','Sub-Saharan','OECD','Fragile','Heavily',
            'Least','Low','Upper','High','Middle','developing','emerging','Baltics',
            'South Asia','Latin','countries','Americas','Africa','Asia','Europe','America']

    by_country = defaultdict(list)
    for row in data:
        c = row.get('countryName', '')
        if not any(x in c for x in SKIP):
            by_country[c].append({'year': row['year'], 'value': row['value']})

    pairs = []
    for c, rows in by_country.items():
        valid = {r['year']: r['value'] for r in rows if r['value'] is not None}
        v2000 = valid.get(2000) or valid.get(2001)
        v_recent = valid.get(2023) or valid.get(2022) or valid.get(2021) or valid.get(2024)
        if v2000 is not None and v_recent is not None:
            pairs.append({'n': c, 'a': round(v2000, 1), 'b': round(v_recent, 1)})

    selected = [p for p in pairs if p['n'] in [
        'Bhutan','Congo, Dem. Rep.','Albania','Ethiopia','Cameroon','Georgia',
        'Iceland','Costa Rica','Ecuador','Angola','Colombia','Austria','Brazil','Canada','Ghana'
    ]]
    selected.sort(key=lambda x: x['b'], reverse=True)
    print(f"Selected {len(selected)} countries")
    for p in selected:
        print(f"  {p['n']}: {p['a']}% -> {p['b']}% (change: {p['b']-p['a']:+.1f} pp)")
    return by_country, pairs, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares exactly two time points, emphasizes direction of change
        - **Country selection**: Countries with >30% hydro share in either year, covering all continents
        - **Color**: Warm (orange) = large decline in hydro share (diversified); cool = stable/gained
        - **Story**: Some nations (Bhutan, DRC, Albania) remain almost 100% hydro; others
          (Ghana, Brazil, Cameroon) diversified sharply as grids grew and drought risk mounted
        - **Key outlier**: Ghana dropped 53.6 pp — Akosombo Dam droughts forced thermal expansion
        """
    )
    return


@app.cell
def _(json, selected):
    chart_data = [{'n': p['n'].replace('Congo, Dem. Rep.', 'D.R. Congo'), 'a': p['a'], 'b': p['b']} for p in selected]
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
