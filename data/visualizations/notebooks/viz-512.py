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
        # Stock Market Capitalization Trend Lines — Methodology

        Trend lines showing stock market cap (% of GDP) for 9 countries, 2000–2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--CM-MKT-LCAP-GD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = ['Japan', 'Germany', 'China', 'India', 'Canada', 'Korea, Rep.',
              'Brazil', 'Australia', 'Chile', 'France', 'Indonesia']
    countries = {}
    for row in data:
        c = row['countryName']
        if c in target and row['value'] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][row['year']] = round(row['value'], 1)
    print(f"Countries extracted: {list(countries.keys())}")
    return countries, target


@app.cell
def _(countries, target):
    result = []
    for c in target:
        if c not in countries:
            continue
        pts = [{'y': y, 'v': countries[c][y]} for y in range(2000, 2024) if y in countries[c]]
        if len(pts) >= 15:
            name = 'South Korea' if c == 'Korea, Rep.' else c
            result.append({'n': name, 'pts': pts})
    result.sort(key=lambda x: -x['pts'][-1]['v'])
    print(f"Series with 15+ annual points: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['pts'][0]['v']} ({r['pts'][0]['y']}) -> {r['pts'][-1]['v']} ({r['pts'][-1]['y']})")
    return (result,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how stock market depth evolved year-by-year
        - **Country selection**: 9 major emerging and developed economies with consistent 2000+ data
        - **Notable**: Canada and Australia above 100% since 2000; India surged in 2007 and 2018; South Korea doubled
        - **Annotation**: 2008 global financial crisis shows simultaneous crash across all markets
        """
    )
    return


if __name__ == "__main__":
    app.run()
