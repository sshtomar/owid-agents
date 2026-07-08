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
        # Nuclear Electricity Production -- Methodology

        Tracks the share of electricity generated from nuclear sources for
        key countries from 1990 to 2024. Shows France's dominance, Japan's
        Fukushima collapse, Germany's phase-out, and emerging nuclear nations.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    target = ["France", "Belgium", "Hungary", "Finland", "Czechia",
              "Korea, Rep.", "Japan", "Germany", "Sweden", "United States"]
    years = list(range(1990, 2025))

    chart_data = []
    for country in target:
        if country in by_country:
            vals = by_country[country]
            series = [round(vals[y], 1) if y in vals else None for y in years]
            chart_data.append({"n": country, "s": series, "y0": 1990, "step": 1})
            print(f"{country}: {series[-5:]}")

    return chart_data, by_country, target, years


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
