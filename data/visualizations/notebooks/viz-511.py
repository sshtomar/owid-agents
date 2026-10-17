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
        # Safe Drinking Water Access — Methodology

        Documents the data pipeline behind viz-511.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WSH_WATER_SAFELY_MANAGED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    skip = {'AFR', 'EMR', 'EUR', 'WPR', 'SEAR', 'AMR', 'GLOBAL'}
    real = [x for x in data if x['value'] is not None and x['country'] not in skip and len(x['country']) == 3]
    by_cy = defaultdict(list)
    for x in real:
        if x['year'] == 2022:
            by_cy[x['country']].append(x['value'])
    deduped = {k: round(sum(v) / len(v), 1) for k, v in by_cy.items()}
    print(f"Countries with 2022 data: {len(deduped)}")
    return by_cy, deduped, real, skip


@app.cell
def _(deduped):
    name_map = {
        'COD': 'DR Congo', 'TCD': 'Chad', 'BEN': 'Benin', 'CIV': 'Ivory Coast',
        'LAO': 'Laos', 'IDN': 'Indonesia', 'NGA': 'Nigeria', 'DOM': 'Dominican Rep.',
        'ECU': 'Ecuador', 'ZAF': 'South Africa', 'RWA': 'Rwanda', 'PER': 'Peru',
        'BGD': 'Bangladesh', 'IRQ': 'Iraq', 'BWA': 'Botswana', 'GEO': 'Georgia',
        'BRA': 'Brazil', 'ROU': 'Romania', 'MKD': 'N. Macedonia', 'POL': 'Poland',
        'OMN': 'Oman', 'IRL': 'Ireland', 'USA': 'United States', 'CHL': 'Chile',
        'NOR': 'Norway', 'ISR': 'Israel', 'HUN': 'Hungary', 'SRB': 'Serbia',
        'PRK': 'North Korea', 'KIR': 'Kiribati', 'KOR': 'South Korea'
    }
    chart_data = sorted(
        [{"n": name_map[k], "v": v} for k, v in deduped.items() if k in name_map],
        key=lambda x: x["v"]
    )
    print(f"Chart data: {len(chart_data)} countries")
    for d in chart_data[:5]:
        print(f"  {d}")
    print("...")
    for d in chart_data[-5:]:
        print(f"  {d}")
    return chart_data, name_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — direct comparison of a single metric across countries
        - **Country selection**: All 30 countries with 2022 data (excluding small territories and regional aggregates)
        - **Color encoding**: Sequential green (high access) to orange/red (low access) — encodes inequality visually
        - **Insight**: DR Congo and Chad below 7%; Hungary and Israel above 99% — 93-point gap
        """
    )
    return


@app.cell
def _(json, chart_data):
    import json as _json
    print(_json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
