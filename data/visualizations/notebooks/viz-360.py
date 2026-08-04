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
        # Overweight Children Under 5: ~2000 vs ~2019 — Methodology

        Slope chart comparing child overweight prevalence near 2000 and 2019
        across 40 countries, highlighting the nutrition transition in middle-income countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-OWGH-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {raw['meta']['title']}")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict
    exclude_kw = [
        "IDA", "IBRD", "Sub-Saharan", "Least", "Heavily", "Low income",
        "Lower middle", "Africa Eastern", "Africa Western", "dividend",
        "Fragile", "World", "Upper middle", "East Asia", "South Asia",
        "Latin America", "Middle East", "Europe", "Central Asia",
        "Arab World", "Caribbean", "Pacific", "North America", "OECD",
        "Euro area", "demographic", "developing", "small states", "High income",
        "Post-demographic", "Central Europe", "European Union", "Middle income",
    ]
    by_country = defaultdict(list)
    for r in data:
        name = r["countryName"]
        if any(kw.lower() in name.lower() for kw in exclude_kw):
            continue
        if r["value"] is None:
            continue
        by_country[name].append((r["year"], r["value"]))

    results = []
    for country, series in by_country.items():
        series.sort()
        near_2000 = min(series, key=lambda x: abs(x[0] - 2000))
        near_2019 = min(series, key=lambda x: abs(x[0] - 2019))
        if abs(near_2000[0] - 2000) <= 3 and abs(near_2019[0] - 2019) <= 3:
            name_clean = (country
                .replace("Egypt, Arab Rep.", "Egypt")
                .replace("Iran, Islamic Rep.", "Iran")
                .replace("Gambia, The", "Gambia")
                .replace("Congo, Dem. Rep.", "D.R. Congo")
                .replace("Korea, Dem. People's Rep.", "North Korea")
                .replace("Dominican Republic", "Dominican Rep."))
            results.append({
                "n": name_clean,
                "a": round(near_2000[1], 1),
                "b": round(near_2019[1], 1),
            })

    results.sort(key=lambda x: x["b"], reverse=True)
    print(f"Countries: {len(results)}")
    for r in results[:10]:
        print(f"  {r['n']}: {r['a']} -> {r['b']} ({round(r['b']-r['a'],1):+.1f})")
    return (results,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — directly shows change between two time points
        - **Country selection**: All 40 countries with matched data near 2000 and 2019
        - **Color**: Red = increase, green = decrease
        - **Story**: China (+5.1pp) and Jordan (+4.7pp) show rapid nutrition transition;
          Georgia (−12pp) and Comoros (−18pp) show remarkable improvement
        """
    )
    return


@app.cell
def _(json, results):
    print(json.dumps(results, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
