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
    mo.md("# Wind Electricity Generation — Methodology\n\nTrend lines for the top 10 wind-generating countries, 2000–2025. Data from Ember Yearly Electricity Data.")
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-WIND.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    top_countries = ["China", "United States of America", "Germany", "Brazil", "India",
                     "United Kingdom", "Spain", "Canada", "France", "Sweden"]
    labels = {"United States of America": "USA", "United Kingdom": "UK"}

    by_country = {}
    for row in [d for d in data if d["countryName"] in top_countries and d["value"] is not None]:
        by_country.setdefault(row["countryName"], {})[row["year"]] = row["value"]

    chart_data = []
    for c in top_countries:
        if c not in by_country:
            continue
        years = list(range(2000, 2026))
        series = [round(by_country[c].get(y, 0), 2) for y in years]
        chart_data.append({"n": labels.get(c, c), "s": series, "y0": 2000, "step": 1})

    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
