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
        # Consumer Price Inflation Surge 2015–2024 — Methodology

        Trend lines showing the synchronized global inflation surge in 2021–22 across 8 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FP-CPI-TOTL-ZG.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = {
        'Germany': 'Germany', 'France': 'France', 'Brazil': 'Brazil',
        'Japan': 'Japan', 'Korea, Rep.': 'South Korea', 'Australia': 'Australia',
        'India': 'India', 'Ethiopia': 'Ethiopia'
    }
    from collections import defaultdict
    by_country = defaultdict(list)
    for r in data:
        if r['value'] is not None and r['countryName'] in targets and 2015 <= r['year'] <= 2024:
            by_country[r['countryName']].append({'y': r['year'], 'v': round(r['value'], 2)})
    chart_data = []
    for orig, disp in targets.items():
        pts = sorted(by_country.get(orig, []), key=lambda x: x['y'])
        if len(pts) >= 7:
            chart_data.append({'n': disp, 'pts': pts})
            peak = max(pts, key=lambda x: x['v'])
            print(f"  {disp}: peak {peak['v']:.1f}% in {peak['y']}")
    return by_country, chart_data, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the synchronized global inflation wave over 10 years
        - **Country selection**: Mix of high-income (Germany, France, Australia, Japan, South Korea), emerging (Brazil, India), and high-inflation (Ethiopia) for full range
        - **Time range**: 2015–2024 — captures pre-surge stability, the 2021–22 spike, and post-spike cooling
        - **Key story**: Countries that had near-zero inflation (Germany, France, Japan) suddenly surged to 5–7% in 2022; Ethiopia's structural inflation dwarfs all
        - **Zero reference**: Dashed horizontal line at 0% anchors the chart
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
