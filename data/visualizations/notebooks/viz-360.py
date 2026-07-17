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
        # PM2.5 Air Pollution Trend Lines — Methodology

        Trend line chart showing mean annual PM2.5 exposure across 10 countries, 1990–2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-ATM-PM25-MC-M3.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    focus = {
        'China': 'China', 'India': 'India', 'Bangladesh': 'Bangladesh',
        'Germany': 'Germany', 'France': 'France', 'Brazil': 'Brazil',
        'Iran, Islamic Rep.': 'Iran', 'Iraq': 'Iraq', 'Indonesia': 'Indonesia', 'Japan': 'Japan'
    }
    result = {}
    for p in data:
        n = p['countryName']
        if n in focus and p.get('value') is not None and (p['year'] % 3 == 0 or p['year'] in [1990, 2023]):
            label = focus[n]
            if label not in result:
                result[label] = {'n': label, 'pts': []}
            if p['year'] not in {pt['y'] for pt in result[label]['pts']}:
                result[label]['pts'].append({'y': p['year'], 'v': round(p['value'], 1)})
    final = [{'n': result[l]['n'], 'pts': sorted(result[l]['pts'], key=lambda x: x['y'])}
             for l in ['Bangladesh', 'Iraq', 'India', 'Iran', 'China', 'Indonesia', 'Brazil', 'Germany', 'France', 'Japan']
             if l in result]
    for s in final:
        p1990 = next((p['v'] for p in s['pts'] if p['y'] == 1990), None)
        p2023 = s['pts'][-1]['v']
        print(f"{s['n']}: {p1990} (1990) -> {p2023} (2023) [{p2023-p1990:+.1f}]")
    return final, focus, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectories rather than just endpoints
        - **Country selection**: Mix of high-burden improvers (China), stagnant high-burden (India, Bangladesh), and improvers (Germany, France, Brazil)
        - **WHO limit annotation**: 5 µg/m³ line shows how far most countries are from safe levels
        - **Color**: Red for persistently high, green for improving, blue for stable/low
        - **3-year sampling**: Reduces short-term variability (dust storms, fires) while showing trend
        """
    )
    return


@app.cell
def _(final, json):
    print(json.dumps(final, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
