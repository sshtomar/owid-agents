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
        # Severe Child Wasting Trends — Methodology

        Documents the data pipeline behind viz-512.
        Shows severe wasting prevalence (weight-for-height < -3 SD) in children under 5
        for countries with the highest burden and longest time series.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NUTRITION_WH_3.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(lambda: defaultdict(list))
    for p in data:
        if p.get('value') is not None:
            by_country[p['country']][p['year']].append(p['value'])

    name_map = {
        'MLI': 'Mali', 'MRT': 'Mauritania', 'IND': 'India',
        'KHM': 'Cambodia', 'BGD': 'Bangladesh', 'BEN': 'Benin',
        'GHA': 'Ghana', 'NPL': 'Nepal', 'YEM': 'Yemen', 'TCD': 'Chad'
    }
    selected_codes = ['MLI', 'MRT', 'IND', 'KHM', 'BGD', 'BEN', 'GHA', 'NPL', 'YEM', 'TCD']

    result = []
    for code in selected_codes:
        year_data = by_country[code]
        pts = []
        for year in sorted(year_data.keys()):
            vals = year_data[year]
            avg = round(sum(vals) / len(vals), 2)
            pts.append({'y': year, 'v': avg})
        result.append({'n': name_map[code], 'pts': pts})
        print(f"{name_map[code]}: {len(pts)} points, max={max(p['v'] for p in pts):.1f}%")
    return by_country, code, name_map, pts, result, selected_codes


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — irregular time series (survey data), so using explicit point-year pairs
        - **Country selection**: 10 countries with highest peak wasting AND at least 7 survey rounds
        - **Key story**: Mali had peak 12.9% in 1996; India remains stubbornly high at ~7-8%; Yemen
          shows sharp uptick during conflict; Bangladesh has improved significantly from 7% to 1.8%
        - **Color**: By peak wasting (warm = highest burden)
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
