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
        # Who Receives the Most Foreign Aid? ODA Per Capita, 2000–2023 -- Methodology

        Trend lines showing net official development assistance (ODA)
        received per capita (current US$) for top consistent recipients.
        Source: World Bank (DT.ODA.ODAT.PC.ZS).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--DT-ODA-ODAT-PC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} rows")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict

    exclude = ['Africa', 'Asia', 'Europe', 'World', 'income', 'IBRD', 'IDA',
               'Latin', 'East', 'South', 'North', 'Sub', 'states', 'Central', 'small',
               'Pacific', 'Caribbean', 'fragile', 'HIPC', 'Least', 'OECD', 'Arab',
               'Heavily', 'Island']

    by_ctry = defaultdict(dict)
    for r in data:
        nm = r['countryName']
        if r['value'] is not None and not any(x.lower() in nm.lower() for x in exclude):
            by_ctry[nm][r['year']] = r['value']

    target = ['Dominica', 'Kiribati', 'Cabo Verde', 'Jordan', 'Bhutan',
              'Djibouti', 'Georgia', 'Afghanistan', 'Iraq', 'Bosnia and Herzegovina']

    years = list(range(2000, 2024))
    series_data = []
    for name in target:
        if name in by_ctry:
            pts = [{'y': y, 'v': round(by_ctry[name][y], 0)}
                   for y in years if y in by_ctry[name]]
            if len(pts) >= 15:
                series_data.append({'n': name, 'pts': pts})

    print(f"Series: {len(series_data)}")
    for s in series_data:
        last = s['pts'][-1]
        print(f"  {s['n']}: {len(s['pts'])} pts, latest {last['v']:.0f} ({last['y']})")
    return series_data, by_ctry, target, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — annual time series 2000–2023
        - **Countries**: Top 10 consistent ODA recipients per capita since 2000
        - **Highlights**: Dominica spiked post-Hurricane Maria (2017); Iraq had massive
          post-invasion inflows 2003–2008; Kiribati receives sustained high support as
          a small island state threatened by sea-level rise
        """
    )
    return


@app.cell
def _(json, series_data):
    print(json.dumps(series_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
