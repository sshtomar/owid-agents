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
        # The Factory Floor Shifts East — Methodology

        Documents the data pipeline for viz-365: manufacturing value added
        as % of GDP, 1990–2023, trend lines for 6 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-MANF-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    by_country = defaultdict(list)
    for row in data:
        by_country[row['countryName']].append({'year': row['year'], 'value': row['value']})

    countries = {
        'China': 'China',
        'Korea, Rep.': 'South Korea',
        'Germany': 'Germany',
        'Japan': 'Japan',
        'Bangladesh': 'Bangladesh',
        'Australia': 'Australia'
    }

    series = []
    for orig, label in countries.items():
        rows = by_country.get(orig, [])
        pts = [{'y': r['year'], 'v': round(r['value'], 2)}
               for r in rows if r['value'] is not None and 1990 <= r['year'] <= 2023]
        pts.sort(key=lambda x: x['y'])
        if pts:
            series.append({'n': label, 'pts': pts})
            print(f"{label}: {pts[0]['y']}-{pts[-1]['y']}, range {min(p['v'] for p in pts):.1f}-{max(p['v'] for p in pts):.1f}%")
    return by_country, countries, series


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows continuous trajectory over 33 years
        - **Country selection**: Represents deindustrializing West (Germany, Japan, Australia),
          stable East Asia (South Korea, China), and industrializing South Asia (Bangladesh)
        - **Color**: Each country gets a distinct color; warm for risers, cool for decliners
        - **Story**: The clearest trend is Australia's collapse (14% → 5%) and Bangladesh's
          rise (13% → 22%). China peaked at 32% in 2006 and has declined as services grew.
        - **Note**: US, UK, Vietnam missing from World Bank dataset for this indicator
        """
    )
    return


@app.cell
def _(json, series):
    # Export without colors (HTML assigns them)
    export = [{'n': s['n'], 'pts': s['pts']} for s in series]
    print(json.dumps(export, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
