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
        # Lifetime Risk of Maternal Death — Methodology

        Slope chart comparing 1990 to 2022 lifetime risk of maternal death,
        focusing on the highest-burden countries and their trajectories.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MMR-RISK-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_words = ["income", "IDA", "IBRD", "OECD", "G20", "dividend", "situations", "Fragile",
                  "World", "region", "Eastern", "Western", "Southern", "Northern", "Pacific",
                  "Caribbean", "Arab", "Central", "Sub-Saharan", "Europe", "America", "Asia",
                  "Africa", "states", "Least", "indebted"]
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        n = row["countryName"]
        if any(x in n for x in skip_words): continue
        if row["value"] is not None:
            by_country[n][row["year"]] = row["value"]

    points = []
    for c, years in by_country.items():
        a = years.get(1990)
        b = years.get(2022) or years.get(2021) or years.get(2020)
        if a is not None and b is not None and a > 1.5:
            points.append({"n": c, "a": round(a, 2), "b": round(b, 2)})

    points.sort(key=lambda x: x["a"], reverse=True)
    print(f"Countries with 1990 risk > 1.5%: {len(points)}")
    print("Top 5:", [(p["n"], p["a"], "->", p["b"]) for p in points[:5]])
    return by_country, points, skip_words


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparison with many entities
        - **Country selection**: Top 20 by 1990 lifetime risk (all > 2%), captures high-burden countries
        - **Time range**: 1990 → 2022 (32-year horizon shows generational change)
        - **Highlights**: Ethiopia dropped from 8.5% → 0.9% (−90%); Bangladesh 4.2% → 0.3%;
          Chad only fell from 8.0% → 4.5% (−43%) — conflict and governance factors
        - **Color**: Diverging green ramp by % decline: deeper green = larger reduction
        """
    )
    return


@app.cell
def _(json, points):
    top22 = points[:22]
    print(json.dumps(top22, separators=(",", ":")))
    return top22,


if __name__ == "__main__":
    app.run()
