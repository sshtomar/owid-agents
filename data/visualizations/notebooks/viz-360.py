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
        # Alcohol Consumption per Capita -- Methodology

        Compares total alcohol consumption per capita (liters of pure alcohol)
        between 2000 and 2019 across the top-consuming countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ALC-PCAP-LI.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for p in data:
        if p["value"] is not None:
            by_country[p["countryName"]][p["year"]] = p["value"]

    slope_data = []
    for country, yr_dict in by_country.items():
        if 2000 in yr_dict and 2019 in yr_dict:
            slope_data.append({
                "n": country,
                "a": round(yr_dict[2000], 2),
                "b": round(yr_dict[2019], 2)
            })

    exclude = ["income", "World", "region", "IDA", "IBRD", "OECD", "dividend",
               "states", "Europe", "Latin", "East Asia", "South Asia",
               "Sub-Saharan", "Pacific", "Caribbean", "North Africa", "Arab",
               "Euro area", "European Union", "North America", "Central Europe"]
    individual = [s for s in slope_data if not any(w in s["n"] for w in exclude)]
    individual.sort(key=lambda x: -x["b"])
    print(f"Countries with 2000+2019 data: {len(individual)}")
    for s in individual[:25]:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['b']-s['a']:+.2f})")
    return individual, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows 2000 vs 2019 comparison with change direction
        - **Country selection**: Top 20 countries by 2019 consumption
        - **Time range**: 2000 vs 2019 (avoids 2020 COVID disruption)
        - **Highlights**: Most W. European countries reduced consumption; Georgia and Cambodia rose sharply
        """
    )
    return


@app.cell
def _(json, individual):
    selected = individual[:20]
    print(json.dumps(selected))
    return (selected,)


if __name__ == "__main__":
    app.run()
