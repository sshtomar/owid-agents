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
        # Bioenergy Electricity Generation — Methodology

        Trend lines for top 10 bioenergy electricity producers, 2000–2024 (viz-515).
        Bioenergy includes biomass combustion, biogas, and waste-to-energy.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--GEN-BIOENERGY.json"
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

    top10 = [
        "China", "Brazil", "Germany", "United States of America", "Japan",
        "United Kingdom", "India", "Indonesia", "South Korea", "Italy"
    ]
    name_map = {
        "United States of America": "USA",
        "United Kingdom": "UK",
        "South Korea": "S. Korea",
    }

    years = list(range(2000, 2025))
    chart_data = []
    for name in top10:
        display = name_map.get(name, name)
        if name in by_country:
            series = [round(by_country[name].get(y, 0) or 0, 2) for y in years]
            chart_data.append({"n": display, "s": series, "y0": 2000})

    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
