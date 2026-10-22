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
        # Stock Market Capitalization — Methodology

        Trend lines showing stock market cap as % of GDP for 9 major economies
        from 1990 to 2024.
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
    selected = ['Japan', 'China', 'India', 'France', 'Germany',
                'Korea, Rep.', 'Brazil', 'Australia', 'Canada']
    series = {}
    for r in data:
        n = r['countryName']
        if n in selected and r.get('value') is not None and r.get('year', 0) >= 1990:
            if n not in series:
                series[n] = {}
            series[n][r['year']] = r['value']
    filtered = [
        {'n': n, 'pts': [{'y': y, 'v': round(v, 1)} for y, v in sorted(series[n].items())]}
        for n in selected if n in series
    ]
    print(f"Countries extracted: {len(filtered)}")
    for s in filtered:
        pts = s['pts']
        print(f"  {s['n']}: {pts[0]['y']}-{pts[-1]['y']}, latest={pts[-1]['v']}%")
    return (filtered,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — reveals booms, busts, and long-term trajectories
        - **Country selection**: 9 major economies with different financial development stories
        - **Notable events**: Japan's bubble-era peak (~90% in 1990), 2000 dot-com bust, 2008 crash (marked), India's extraordinary 2018 spike (161%)
        - **Reference line**: 100% of GDP marks the threshold where markets equal the entire economy
        - **Time range**: 1990-2024 (varies by country data availability)
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
