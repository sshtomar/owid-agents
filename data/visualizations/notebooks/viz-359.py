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
        # Nuclear Electricity Slope Chart — Methodology

        Slope chart comparing nuclear electricity share in 1990 vs. ~2023 for 16 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip = ['excluding', 'IDA', 'IBRD', 'income', 'dividend', 'World', 'Euro', 'European',
            'America', 'Africa', 'Asia', 'Arab', 'Pacific', 'Atlantic', 'OECD', 'Caribbean',
            'North', 'South', 'Central', 'Eastern', 'Western', 'Post-', 'Pre-', 'Late-',
            'Early-', 'Low', 'Middle', 'High', 'Upper', 'Lower']
    name_map = {'Korea, Rep.': 'South Korea'}
    c1990 = {}
    c_latest = {}
    for p in data:
        n = p['countryName']
        if any(x in n for x in skip):
            continue
        if p.get('value') is None:
            continue
        if p['year'] == 1990:
            c1990[n] = p['value']
        if p['year'] >= 2020:
            if n not in c_latest or p['year'] > c_latest[n][0]:
                c_latest[n] = (p['year'], p['value'])
    chart_data = []
    for n in set(list(c1990.keys()) + list(c_latest.keys())):
        v90 = c1990.get(n, 0)
        vl = c_latest[n][1] if n in c_latest else 0
        if max(v90, vl) > 0.5:
            label = name_map.get(n, n)
            chart_data.append({'n': label, 'a': round(v90, 1), 'b': round(vl, 1)})
    chart_data.sort(key=lambda x: x['b'], reverse=True)
    print(f"Chart data: {len(chart_data)} countries with nuclear power")
    for r in chart_data:
        print(f"  {r['n']}: {r['a']}% -> {r['b']}%")
    return c1990, c_latest, chart_data, name_map, skip


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — comparing two endpoints to highlight directional change
        - **Year selection**: 1990 (pre-collapse of Soviet nuclear programs) vs. ~2023 (latest available)
        - **Country selection**: All countries with meaningful nuclear share (>0.5%) in either year
        - **Color**: Encodes change direction — green = growing, red = declining
        - **Key stories**: Germany's exit (27.7% -> 1.4%), Japan's Fukushima impact, new entrants Belarus/Armenia
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
