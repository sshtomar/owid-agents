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
        # Old-Age Dependency Ratio Trend Lines — Methodology

        Trend line chart showing elderly dependants per 100 working-age people
        across 10 countries from 1960 to 2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    focus = ['Japan', 'Italy', 'Germany', 'France', 'Korea, Rep.', 'China', 'Brazil', 'India', 'Angola', 'Ethiopia']
    labels = {'Korea, Rep.': 'South Korea'}
    result = {}
    for p in data:
        n = p['countryName']
        if n in focus and p.get('value') is not None and (p['year'] % 5 == 0 or p['year'] == 2024):
            label = labels.get(n, n)
            if label not in result:
                result[label] = {'n': label, 'pts': []}
            if p['year'] not in {pt['y'] for pt in result[label]['pts']}:
                result[label]['pts'].append({'y': p['year'], 'v': round(p['value'], 1)})
    final = [{'n': result[l]['n'], 'pts': sorted(result[l]['pts'], key=lambda x: x['y'])}
             for l in ['Japan', 'Italy', 'Germany', 'France', 'South Korea', 'China', 'Brazil', 'India', 'Angola', 'Ethiopia']
             if l in result]
    for s in final:
        vals = [p['v'] for p in s['pts']]
        print(f"{s['n']}: {vals[0]:.1f}% (1960) -> {vals[-1]:.1f}% (2024)")
    return final, focus, labels, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 64 years of annual data, best shown as continuous trajectories
        - **Country selection**: Aging leaders (Japan, Italy, Germany), rapid risers (South Korea, China), slow risers (India), flat (Angola, Ethiopia)
        - **5-year sampling**: Reduces noise while preserving trend shape
        - **Highlights**: Japan now has 50.7% vs Ethiopia's 5.6% — a 9x gap that didn't exist in 1960
        """
    )
    return


@app.cell
def _(final, json):
    print(json.dumps(final, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
