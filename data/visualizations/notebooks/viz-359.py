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
        # Old-Age Dependency Ratio, 1970–2024 — Methodology

        This notebook documents the data pipeline behind viz-359.
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
    from collections import defaultdict
    selected = ['Japan', 'Germany', 'Italy', 'France', 'Brazil', 'China', 'India', 'Indonesia', 'Korea, Rep.']
    label_map = {'Korea, Rep.': 'South Korea'}

    by_country = defaultdict(dict)
    for row in data:
        if row['value'] is not None and row['countryName'] in selected and 1970 <= row['year'] <= 2024:
            by_country[row['countryName']][row['year']] = row['value']

    years = list(range(1970, 2025))
    chart_data = []
    for c in selected:
        if not by_country[c]:
            continue
        pts = [{'y': y, 'v': round(by_country[c][y], 1)} for y in years if y in by_country[c]]
        chart_data.append({'n': label_map.get(c, c), 'pts': pts})

    print(f"Countries: {len(chart_data)}")
    for item in chart_data:
        print(f"  {item['n']}: {item['pts'][0]['v']} (1970) -> {item['pts'][-1]['v']} (latest)")
    return chart_data, by_country, years, selected, label_map, defaultdict


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the long-run demographic shift over 54 years
        - **Country selection**: 9 countries spanning aging leaders (Japan, Italy) and still-young populations (India, Indonesia)
        - **Time range**: 1970–2024 (full history available)
        - **Highlights**: Japan went from 10% to 50.7%; South Korea is now on a steeper trajectory than Japan was in the 1980s
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
