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
        # Inflation History: Consumer Prices -- Methodology

        Trend lines for 10 countries showing annual inflation (% CPI change),
        1970-2024. Values capped at 100% for readability (Bolivia, Israel, and
        Brazil experienced hyperinflation well above this ceiling). Highlights
        contrasting inflation experiences across income levels and regions.
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
    selected = ['Germany', 'Japan', 'Israel', 'Bolivia', 'Brazil',
                'Iran, Islamic Rep.', 'Colombia', 'Indonesia', 'India', 'Iceland']
    display_names = {'Iran, Islamic Rep.': 'Iran'}
    by_country = {}
    for row in data:
        if row['value'] is None:
            continue
        n = row['countryName']
        if n not in by_country:
            by_country[n] = {}
        by_country[n][row['year']] = row['value']

    chart_data = []
    for name in selected:
        if name not in by_country:
            continue
        pts = [{'y': y, 'v': round(min(by_country[name][y], 100), 2)}
               for y in sorted(by_country[name]) if 1970 <= y <= 2024]
        chart_data.append({'n': display_names.get(name, name), 'pts': pts})

    print(f"Countries: {[d['n'] for d in chart_data]}")
    return by_country, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows time series for 10 countries
        - **Country selection**: Diverse experiences (hyperinflation, near-zero, chronic)
        - **Time range**: 1970-2024 (oil shocks, 1980s hyperinflation, 2022 spike)
        - **Cap**: Values above 100% capped for axis readability
        """
    )
    return


if __name__ == "__main__":
    app.run()
