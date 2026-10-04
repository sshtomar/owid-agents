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
        # Severe Wasting in Children Under 5 -- Methodology

        Compares severe wasting prevalence (% of children under 5)
        between early 2000s and most recent survey year.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-SVR-WAST-ZS.json"
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
        early_years = [y for y in yr_dict if 2000 <= y <= 2010]
        recent_years = [y for y in yr_dict if y >= 2018]
        if early_years and recent_years:
            early_yr = early_years[0]
            recent_yr = recent_years[-1]
            v_old = yr_dict[early_yr]
            v_new = yr_dict[recent_yr]
            if v_old > 0 and v_new > 0:
                slope_data.append({"n": country, "a": round(v_old, 2), "b": round(v_new, 2)})

    exclude = ["income", "World", "region", "IDA", "IBRD", "OECD", "dividend",
               "states", "Europe", "Latin", "East Asia", "South Asia",
               "Sub-Saharan", "Pacific", "Caribbean", "North Africa", "Arab"]
    individual = [s for s in slope_data if not any(w in s["n"] for w in exclude)]
    individual.sort(key=lambda x: -x["a"])
    print(f"Countries for chart: {len(individual)}")
    for s in individual[:20]:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['b']-s['a']:+.1f}pp)")
    return individual, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- compares two time points showing direction of change
        - **Country selection**: Top 20 countries by early 2000s wasting rate (most affected)
        - **Time range**: Early 2000s baseline vs most recent survey (2018-2024)
        - **Highlights**: India is the notable outlier -- wasting slightly increased. Most others improved.
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
