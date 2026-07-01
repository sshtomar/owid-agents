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
        # Cholera Deaths 1950–2016 — Methodology

        Area chart showing reported global cholera deaths per year from 1950 to 2016.
        The 1953 spike (124,242 deaths, dominated by India) is clipped at 30,000 in the
        visual but shown in full on hover. Key epidemiological milestones annotated.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--CHOLERA_0000000002.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_year = {}
    for r in data:
        if r['value']:
            by_year[r['year']] = by_year.get(r['year'], 0) + r['value']

    series = [{'y': yr, 'v': round(by_year[yr])} for yr in sorted(by_year)]

    print("Global total by year:")
    for s in series:
        if s['v'] > 1000:
            print(f"  {s['y']}: {s['v']:,}")

    print(f"\nTotal years: {len(series)}, range: {series[0]['y']}–{series[-1]['y']}")
    print(f"Peak year: 1953 with {by_year[1953]:,} deaths")
    return series, by_year


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Area/bar chart with hover crosshair — time series showing epidemic waves
        - **Clipping**: 1953 spike is clipped at 30,000 for chart legibility, full value shown in tooltip
        - **Annotations**: 7th pandemic start (1961 El Tor strain), Latin America resurgence (1991)
        - **Story**: India's 1953 epidemic dominated the last years of the 6th pandemic.
          The 7th pandemic drove persistent deaths from 1961 through the 1990s.
          Modern sanitation and oral rehydration therapy cut deaths dramatically by 2010s.
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
