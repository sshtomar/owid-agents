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
        # The Nuclear Fork -- Methodology

        Nuclear electricity share (% of total) 1990-2023 for 7 countries.
        Source: World Bank EG.ELC.NUCL.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = {}
    for pt in data:
        c = pt["countryName"]
        if c not in countries:
            countries[c] = {}
        if pt["value"] is not None:
            countries[c][str(pt["year"])] = round(pt["value"], 2)

    selected = ["France", "Belgium", "Finland", "Czechia", "Korea, Rep.", "Japan", "Germany"]
    labels = {"Korea, Rep.": "Korea"}
    years = list(range(1990, 2024))
    chart_data = []
    for c in selected:
        if c in countries:
            series = [countries[c].get(str(y)) for y in years]
            chart_data.append({"n": labels.get(c, c), "s": series})
    print(f"Chart data: {len(chart_data)} countries x {len(years)} years")
    print(f"Germany 2023: {countries['Germany'].get('2023')}%")
    print(f"Japan 2011: {countries['Japan'].get('2011')}% -> 2012: {countries['Japan'].get('2012')}%")
    return chart_data, countries, labels, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows diverging trajectories after Fukushima 2011
        - **Countries**: France (dominant), Germany (deliberate exit), Japan (Fukushima cliff),
          Korea and Finland (stable/rising), Czechia (rising), Belgium (declining)
        - **Annotation**: Vertical line at 2011 labeled "Fukushima"
        - **Key insight**: Germany went from 28% to 1.4%; Japan fell from 25% to near zero
          then slowly recovered; Czechia climbed to 39%
        """
    )
    return


if __name__ == "__main__":
    app.run()
