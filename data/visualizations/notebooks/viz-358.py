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
        # Mineral Rents as % of GDP: 2000 vs. 2020 — Methodology

        Documents the data pipeline behind viz-358.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-MINR-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_keywords = [
        "Africa", "Asia", "Europe", "America", "Pacific", "Arab", "Caribbean",
        "income", "World", "Central", "Eastern", "Western", "Northern", "Southern",
        "OECD", "Euro", "Fragile", "Heavily", "IBRD", "IDA", "Small", "dividend",
        "states", "countries", "area", "region", "demographic"
    ]
    individual = [
        d for d in data
        if d["value"] is not None
        and not any(k in d["countryName"] for k in agg_keywords)
    ]
    print(f"Individual country rows: {len(individual)}")
    return agg_keywords, individual


@app.cell
def _(individual):
    from collections import defaultdict
    by_country_year = defaultdict(dict)
    for row in individual:
        by_country_year[row["countryName"]][row["year"]] = row["value"]

    slope_data = []
    for name, ydict in by_country_year.items():
        a = ydict.get(2000) or ydict.get(1999) or ydict.get(2001)
        b = ydict.get(2020) or ydict.get(2019) or ydict.get(2021)
        if a is not None and b is not None:
            slope_data.append({"n": name, "a": round(a, 2), "b": round(b, 2)})

    top18 = sorted(slope_data, key=lambda x: -x["b"])[:18]
    print("Top 18 by 2020 value:")
    for item in top18:
        print(f"  {item['n']}: {item['a']}% -> {item['b']}%")
    return by_country_year, slope_data, top18


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — directly shows change between two snapshots
        - **Year selection**: 2000 and 2020 (pre-COVID for stable reading, 20-year span)
        - **Entity selection**: Top 18 countries by 2020 mineral rent share
        - **Color encoding**: Red/orange for rising dependence, green for declining
        - **Key insight**: Congo DRC jumped from near-zero to 5.6% — cobalt and coltan boom.
          Guyana actually fell (gold extraction peaked earlier). Chile stable but Chile's share
          comes from copper, the foundation of its development model.
        """
    )
    return


@app.cell
def _(json, top18):
    print(json.dumps(top18, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
