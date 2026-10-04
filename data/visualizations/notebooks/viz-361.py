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
        # Polio Immunization Coverage -- Methodology

        Compares Pol3 immunization coverage (% of one-year-olds)
        between the early 1980s and 2024 for countries with the biggest gains.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-POL3.json"
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
        early_years = [y for y in yr_dict if y <= 1990]
        recent_years = [y for y in yr_dict if y >= 2022]
        if early_years and recent_years:
            early_yr = min(early_years)
            recent_yr = max(recent_years)
            v_old = yr_dict[early_yr]
            v_new = yr_dict[recent_yr]
            slope_data.append({
                "n": country,
                "a": round(v_old, 1),
                "b": round(v_new, 1),
                "change": v_new - v_old
            })

    exclude = ["income", "World", "region", "IDA", "IBRD", "OECD", "dividend",
               "states", "Europe", "Latin", "East Asia", "South Asia",
               "Sub-Saharan", "Pacific", "Caribbean", "North Africa", "Arab",
               "Africa Western", "Africa Eastern", "Heavily", "Least developed", "demographic", "classified"]
    individual = [s for s in slope_data if not any(w in s["n"] for w in exclude)]
    individual.sort(key=lambda x: -x["change"])
    print(f"Countries with 1980-1990 baseline: {len(individual)}")
    for s in individual[:20]:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['change']:+.0f}pp)")
    return individual, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows the dramatic rise from near-zero to near-universal
        - **Country selection**: 18 countries with biggest absolute gains from early 1980s baseline
        - **Time range**: Earliest available (1980-1985) vs 2024
        - **Highlights**: Bangladesh 1%->97%, Bhutan 4%->99%, India 2%->93% -- one of public health's greatest wins
        """
    )
    return


@app.cell
def _(json, individual):
    selected = individual[:18]
    print(json.dumps([{"n": s["n"], "a": s["a"], "b": s["b"]} for s in selected]))
    return (selected,)


if __name__ == "__main__":
    app.run()
