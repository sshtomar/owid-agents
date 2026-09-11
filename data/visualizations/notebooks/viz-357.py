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
        # Solar Electricity Generation — Methodology

        Trend lines for the top 10 solar-generating countries, 2000–2025.
        Data from Ember Yearly Electricity Data.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-SOLAR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    top_countries = ["China", "United States of America", "India", "Japan", "Germany",
                     "Brazil", "Spain", "Australia", "Italy", "South Korea"]
    labels = {"United States of America": "USA"}

    filtered = [d for d in data if d["countryName"] in top_countries and d["value"] is not None]
    print(f"Filtered to {len(filtered)} points across top 10 countries")
    return filtered, labels, top_countries


@app.cell
def _(filtered, json, labels, top_countries):
    by_country = {}
    for row in filtered:
        c = row["countryName"]
        by_country.setdefault(c, {})[row["year"]] = row["value"]

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
