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
        # Suicide Mortality Rate Trends — Methodology

        Trend lines for 12 countries showing age-standardized suicide mortality
        rates (per 100,000 population) from 2000 to 2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-SUIC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = [
        'Korea, Rep.', 'Japan', 'Belgium', 'France', 'Germany',
        'Belarus', 'Hungary', 'India', 'Brazil', 'Indonesia',
        'Finland', 'Guyana'
    ]
    series = {}
    for row in data:
        n = row.get('countryName', '')
        if n in selected and row.get('value') is not None:
            if n not in series:
                series[n] = {}
            series[n][row['year']] = row['value']
    filtered = [
        {'n': n, 'pts': [{'y': y, 'v': round(v, 2)} for y, v in sorted(series[n].items())]}
        for n in selected if n in series
    ]
    print(f"Countries extracted: {len(filtered)}")
    return (filtered,)


@app.cell
def _(filtered):
    for s in filtered:
        pts = s['pts']
        print(f"{s['n']}: {pts[0]['y']}-{pts[-1]['y']}, range {min(p['v'] for p in pts):.1f}-{max(p['v'] for p in pts):.1f}")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows 22-year trajectories for multiple countries simultaneously
        - **Country selection**: 12 countries with diverse stories: Eastern Europe (Belarus, Hungary — dramatic decline), East Asia (Korea, Japan — high rates), Western Europe (Belgium, France, Germany, Finland — moderate, declining), South Asia (India — stable), Latin America (Brazil — rising slightly), Southeast Asia (Indonesia — very low), Caribbean (Guyana — persistently high)
        - **Time range**: 2000-2021 (full dataset range)
        - **Highlights**: Belarus dropped from 40 to 16; South Korea rose sharply to 35 before declining; Indonesia stays under 2
        """
    )
    return


@app.cell
def _(json, filtered):
    chart_data = filtered
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
