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
        # Wind Electricity Generation — Methodology

        Trend lines showing wind electricity generation for the top 8 producing countries from 2000 to 2025. Data from Ember's Global Electricity Review.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-WIND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    top_countries = ["China", "United States of America", "Germany", "Brazil", "United Kingdom", "India", "Spain", "Canada"]
    labels = {"United States of America": "United States", "United Kingdom": "UK"}

    by_country = {}
    for row in data:
        c = row["countryName"]
        if c in top_countries and row["value"] is not None:
            by_country.setdefault(c, {})[row["year"]] = row["value"]

    for c in top_countries:
        if c in by_country:
            years = sorted(by_country[c].keys())
            print(f"  {c}: {years[0]}-{years[-1]}, 2024={by_country[c].get(2024, 0):.0f} TWh")
    return by_country, labels, top_countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — comparable format to solar viz, shows the parallel wind buildout
        - **Country selection**: Top 8 by 2025 generation; includes Germany and UK for European context
        - **Time range**: 2000–2025
        - **Highlights**: China now generates more wind power than the next 7 countries combined
        """
    )
    return


@app.cell
def _(json, by_country, top_countries, labels):
    years_range = list(range(2000, 2026))
    chart_data = []
    for c in top_countries:
        if c in by_country:
            series = [round(by_country[c].get(y, 0) or 0, 2) for y in years_range]
            chart_data.append({"n": labels.get(c, c), "s": series, "y0": 2000, "step": 1})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
