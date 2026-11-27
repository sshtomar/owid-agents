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
        # Services Value Added (% of GDP) — Methodology

        Tracks the share of GDP coming from the services sector for 10 diverse
        countries, 1960–2024. Shows how economies structurally transform.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-SRV-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregate_patterns = [
        'income', 'region', 'World', '& Pacific', '& Central', 'Middle East',
        'Latin America', 'Sub-Saharan', 'North Africa', 'Euro area', 'South Asia',
        'East Asia', 'Arab World', 'Caribbean small', 'OECD', 'fragile', 'Fragility',
        'IDA', 'IBRD', 'island', 'Small states', 'Heavily', 'Least',
        'demographic', 'Africa Western', 'Africa Eastern', 'Europe &'
    ]
    def is_aggregate(cn):
        return any(x.lower() in cn.lower() for x in aggregate_patterns)

    target = {
        'France': 'France', 'Germany': 'Germany', 'China': 'China',
        'India': 'India', 'Chile': 'Chile', 'Egypt, Arab Rep.': 'Egypt',
        'Botswana': 'Botswana', 'Bangladesh': 'Bangladesh',
        'Costa Rica': 'Costa Rica', 'El Salvador': 'El Salvador'
    }
    country_data = {}
    for row in data:
        cn = row['countryName']
        if cn in target and row['value'] and row['value'] > 0:
            label = target[cn]
            if label not in country_data:
                country_data[label] = {}
            country_data[label][row['year']] = round(row['value'], 1)

    print(f"Countries with data: {list(country_data.keys())}")
    return country_data, is_aggregate, target


@app.cell
def _(country_data):
    countries_summary = []
    for cn, ydata in country_data.items():
        pts = sorted(ydata.items())
        countries_summary.append({
            'country': cn,
            'start_year': pts[0][0],
            'end_year': pts[-1][0],
            'start_val': pts[0][1],
            'end_val': pts[-1][1],
            'n_pts': len(pts)
        })
        print(f"{cn}: {pts[0][0]}({pts[0][1]}%) → {pts[-1][0]}({pts[-1][1]}%)")
    return (countries_summary,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectories of structural transformation
        - **Country selection**: 10 countries across 5 regions showing different development paths
        - **Time range**: 1960–2024 (longest available series)
        - **Highlights**: China's dramatic shift from 23% to 57%; France/Germany already at 60%+ at start
        """
    )
    return


@app.cell
def _(json, country_data):
    chart_data = []
    for label, ydata in sorted(country_data.items()):
        pts = sorted(ydata.items())
        chart_data.append({
            "n": label,
            "s": [v for _, v in pts],
            "y0": pts[0][0]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
