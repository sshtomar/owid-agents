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
        # Gas Electricity Generation — Methodology

        Trend lines showing electricity generation from natural gas (TWh) for
        the top 10 producers globally, 2000–2024 (viz-512).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-GAS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(json, data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]][pt["year"]] = pt["value"]

    top10 = ["United States of America", "Russian Federation (the)", "Japan",
             "Iran (Islamic Republic of)", "China", "Saudi Arabia",
             "Mexico", "Egypt", "South Korea", "Thailand"]

    name_map = {
        "United States of America": "USA",
        "Russian Federation (the)": "Russia",
        "Iran (Islamic Republic of)": "Iran",
        "South Korea": "S. Korea",
    }

    years = list(range(2000, 2025))
    chart_data = []
    for name in top10:
        display = name_map.get(name, name)
        if name in by_country:
            series = [round(by_country[name].get(y, 0) or 0, 1) for y in years]
            chart_data.append({"n": display, "s": series, "y0": 2000})

    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
