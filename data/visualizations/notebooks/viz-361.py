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
        # Threatened Mammal Species by Country — Methodology

        Horizontal bar chart showing the 20 countries with the most IUCN-threatened mammal species (2022).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-MAM-THRD-NO.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    latest = [d for d in data if d["value"] is not None and d["year"] == 2022]
    print(f"Countries with 2022 data: {len(latest)}")
    print(f"Years available: {sorted(set(d['year'] for d in data if d['value'] is not None))}")
    return (latest,)


@app.cell
def _(latest):
    agg_kw = ["income", "dividend", "Sub-Saharan", "East Asia", "Europe", "America", "Pacific",
               "Caribbean", "Arab", "IDA", "IBRD", "OECD", "North", "South Asia", "heavily", "Least",
               "Pre-", "Late-", "Post-", "Low ", "High ", "Upper", "Lower", "small states",
               "Central", "Middle East", "Africa East", "Africa West", "Atlantic", "Euro area", "World"]
    def is_country(name):
        return not any(k.lower() in name.lower() for k in agg_kw)

    countries = [x for x in latest if is_country(x["countryName"])]
    countries.sort(key=lambda x: -x["value"])

    bar_data = [{"n": x["countryName"], "v": int(x["value"])} for x in countries[:20]]
    for row in bar_data:
        print(f'{row["n"]}: {row["v"]}')
    return bar_data, countries, is_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — best for ranked cross-sectional comparison
        - **Country selection**: Top 20 individual countries with most threatened mammals; aggregate
          regions and income groups excluded
        - **Year**: 2022 (most recent available in this dataset)
        - **Story**: Indonesia leads by a large margin (212 species), reflecting its extreme
          biodiversity and habitat loss pressures. Tropical megadiverse countries (Indonesia, India,
          Brazil, China, Australia) dominate the top 5.
        """
    )
    return


@app.cell
def _(json, bar_data):
    print(json.dumps(bar_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
