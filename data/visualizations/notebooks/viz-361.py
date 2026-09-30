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
        # China's Innovation Surge -- Methodology

        Patent applications by residents, 1985-2021.
        Source: World Bank IP.PAT.RESD.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
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
            countries[c][str(pt["year"])] = int(pt["value"])

    selected = ["China", "Japan", "Korea, Rep.", "Germany", "India", "France"]
    labels = {"Korea, Rep.": "Korea"}
    years = list(range(1985, 2022))
    chart_data = []
    for c in selected:
        if c in countries:
            series = [countries[c].get(str(y)) for y in years]
            chart_data.append({"n": labels.get(c, c), "s": series})
    print(f"Chart data: {len(chart_data)} countries")
    print(f"China 2021: {countries['China'].get('2021'):,}")
    print(f"Japan 2021: {countries['Japan'].get('2021'):,}")
    print(f"China share 2021: {countries['China'].get('2021') / 2385200 * 100:.1f}% of world")
    return chart_data, countries, labels, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- China's explosive trajectory vs flat others
        - **Scale**: Linear (not log) to show the visual dominance of China's rise
        - **Countries**: China, Japan (world's 2nd filer in 1990s), Korea, Germany, India, France
        - **Key insight**: China went from 4,065 patents in 1985 to 1.43M in 2021 -- a 350x increase.
          In 2021 China filed 60% of all patents globally.
        """
    )
    return


if __name__ == "__main__":
    app.run()
