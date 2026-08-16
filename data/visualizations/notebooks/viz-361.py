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
        # Gross Savings Sparkline Grid — Methodology

        Documents the data pipeline for viz-361: sparkline grid of gross savings rates
        (% of GDP) for 25 countries, 1990–2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNS-ICTR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries_data = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is None:
            continue
        if c not in countries_data:
            countries_data[c] = {}
        countries_data[c][y] = round(v, 1)

    selected = ['China', 'Indonesia', 'Bangladesh', 'Denmark', 'India', 'Korea, Rep.',
                'Israel', 'Czechia', 'Germany', 'Dominican Republic', 'Hungary', 'Estonia',
                'Australia', 'Italy', 'Finland', 'France', 'Canada', 'Ecuador', 'Chile',
                'Guatemala', 'Kenya', 'Brazil', 'Colombia', 'Greece', 'Ghana']

    print(f"Total dataset countries: {len(countries_data)}")
    for c in selected:
        if c in countries_data:
            pts = sorted(countries_data[c].items())
            recent = [v for y, v in pts if y >= 2020]
            print(f"  {c}: range {pts[0][0]}-{pts[-1][0]}, latest={pts[-1][1]}")
    return countries_data, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — shows 25 countries at once; per-cell normalization
          reveals shape while color encodes absolute level
        - **Country selection**: Mix of high (China, Indonesia, India) and low (Greece, Ghana,
          Colombia) savers, plus major economies
        - **Color encoding**: Each cell's line colored by latest savings rate: green >35%,
          amber 20–28%, red <13%
        - **Story**: East Asian savings discipline (China peaked at 51% in 2008) vs structural
          low savings in Latin America and Southern Europe
        """
    )
    return


@app.cell
def _(json, countries_data, selected):
    name_map = {'Korea, Rep.': 'South Korea'}
    chart_data = []
    for c in selected:
        if c not in countries_data:
            continue
        display = name_map.get(c, c)
        series = [countries_data[c].get(y) for y in range(1990, 2024)]
        filled = []
        last = None
        for v in series:
            if v is not None:
                last = v
            filled.append(last)
        latest = filled[-1]
        earliest = next((v for v in filled if v is not None), None)
        chart_data.append({"n": display, "s": filled, "y0": 1990, "e": earliest, "l": latest})

    print(f"Chart data: {len(chart_data)} countries")
    print(json.dumps(chart_data[0], separators=(",", ":")))
    return chart_data, name_map
