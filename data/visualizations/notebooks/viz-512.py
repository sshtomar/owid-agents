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
        # Women in Unpaid Family Work — Methodology

        Slope chart comparing 1991 to 2022 share of female employment that is
        contributing family work (unpaid, informal, largely agricultural).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-FAM-WORK-FE-ZS.json"
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
                  "Africa", "states", "Least"]
    filtered = [d for d in data if d["value"] is not None and not any(x in d["countryName"] for x in skip_words)]
    print(f"After filtering aggregates: {len(filtered)} rows")
    return filtered, skip_words


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in filtered:
        by_country[row["countryName"]][row["year"]] = row["value"]

    points = []
    for c, years in by_country.items():
        a = years.get(1991) or years.get(1992) or years.get(1993)
        b = years.get(2022) or years.get(2021) or years.get(2020)
        if a is not None and b is not None and a > 5:
            points.append({"n": c, "a": round(a, 1), "b": round(b, 1)})

    points.sort(key=lambda x: x["a"], reverse=True)
    print(f"Countries with a > 5%: {len(points)}")
    print("Top 5:", [(p["n"], p["a"], p["b"]) for p in points[:5]])
    return by_country, points


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — best for before/after comparison across many entities
        - **Country selection**: Top 22 by 1991 value (all > 28%), captures high-burden countries
        - **Time range**: 1991 → 2022 (first vs last reliable year)
        - **Highlights**: Bangladesh dropped 76% → 14% (garment industry); Armenia 38% → 7%;
          Afghanistan stayed high at 84% → 69%; Burkina Faso barely moved
        - **Color**: Diverging ramp by % decline magnitude
        """
    )
    return


@app.cell
def _(json, points):
    top25 = points[:25]
    print(json.dumps(top25, separators=(",", ":")))
    return top25,


if __name__ == "__main__":
    app.run()
