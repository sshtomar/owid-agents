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
        # Nuclear Electricity Production by Country — Methodology

        Trend lines showing nuclear share of electricity production (1990-2024)
        for the top 10 nuclear-dependent countries.
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
    target = {
        'France', 'Hungary', 'Belgium', 'Czechia', 'Finland', 'Bulgaria',
        'Korea, Rep.', 'Armenia', 'Belarus', 'Germany', 'United States',
        'Ukraine', 'Canada', 'Sweden', 'Switzerland', 'Japan'
    }
    by_country = {}
    for x in data:
        if x['countryName'] in target and x['value'] is not None:
            if x['countryName'] not in by_country:
                by_country[x['countryName']] = {}
            by_country[x['countryName']][x['year']] = x['value']
    result = []
    for c, yv in by_country.items():
        pts = [{'y': y, 'v': round(yv[y], 1)} for y in sorted(yv.keys()) if 1990 <= y <= 2024]
        if pts:
            latest = max(p['v'] for p in pts)
            result.append((c, pts, latest))
    result.sort(key=lambda x: -x[2])
    top10 = result[:10]
    print("Countries selected:", [c for c, _, _ in top10])
    return by_country, result, target, top10


@app.cell
def _(json, top10):
    chart_data = [{"n": c, "pts": pts} for c, pts, _ in top10]
    print(json.dumps(chart_data[:1], separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
