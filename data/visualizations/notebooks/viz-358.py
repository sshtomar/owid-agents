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
        # Government Consumption Expenditure (% GDP): 1995 vs 2023 -- Methodology

        Slope chart comparing general government final consumption as a share of GDP
        across 18 countries. Reveals the divide between large Nordic public sectors
        and minimal-state economies in Asia and Africa.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NE-CON-GOVT-ZS.json"
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

    selected_map = {
        "Denmark": "Denmark", "Finland": "Finland", "France": "France",
        "Germany": "Germany", "Belgium": "Belgium", "Austria": "Austria",
        "Canada": "Canada", "Australia": "Australia", "Japan": "Japan",
        "South Korea": "Korea, Rep.", "China": "China", "India": "India",
        "Brazil": "Brazil", "Indonesia": "Indonesia", "Kenya": "Kenya",
        "Bangladesh": "Bangladesh", "Czech Republic": "Czechia", "Hungary": "Hungary"
    }
    name_fix = {"Korea, Rep.": "South Korea", "Czechia": "Czech Republic", "Turkiye": "Turkey"}

    chart_data = []
    for display_name, key in selected_map.items():
        yrs = by_country.get(key, {})
        a = yrs.get(1995) or yrs.get(1994) or yrs.get(1996)
        b = yrs.get(2023) or yrs.get(2022) or yrs.get(2024)
        if a is not None and b is not None:
            chart_data.append({"n": display_name, "a": round(a, 1), "b": round(b, 1)})
            print(f"{display_name}: {a:.1f}% -> {b:.1f}%")

    print(f"\nTotal: {len(chart_data)}")
    return (chart_data, by_country, selected_map, name_fix)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows both the absolute level and the direction of change
        - **Country selection**: 18 countries spanning all income levels and regions
        - **Year pair**: 1995 vs 2023 — 28-year span captures structural shifts
        - **Highlights**: Finland rose 4pp; South Korea and Japan grew significantly;
          Bangladesh and Indonesia remain below 8% throughout
        - **Color**: Warm = rising, cool green = stable, amber/terra = falling
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
