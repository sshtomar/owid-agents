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
        # Mineral Rents as % of GDP — Methodology

        Horizontal bar chart ranking the top 20 countries by mineral rents as a share of GDP
        (most recent year in 2015-2021). Mineral rents measure the economic surplus from
        mining above the cost of extraction — they proxy how heavily a country's income
        depends on finite extractive resources.
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
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None and row["value"] > 0:
            by_country[row["countryName"]][row["year"]] = round(row["value"], 2)

    skip_keywords = ["World","income","Asia","Africa","Europe","America","Pacific","Arab","OECD",
                     "Caribbean","Central","Eastern","Western","Northern","Sahara","Euro","Latin",
                     "Middle","Small","IDA","IBRD","dividend","fragile","island","developing",
                     "Least","developed","Heavily"]
    countries = {}
    for c, yv in by_country.items():
        if any(k.lower() in c.lower() for k in skip_keywords):
            continue
        recent = {y: v for y, v in yv.items() if 2015 <= y <= 2021}
        if recent:
            yr = max(recent.keys())
            countries[c] = (yr, recent[yr])

    top20 = sorted(countries.items(), key=lambda x: x[1][1], reverse=True)[:20]
    result = [{"n": c, "v": v, "y": yr} for c, (yr, v) in top20]
    print(f"Top 20 countries; range: {result[-1]['v']:.2f} – {result[0]['v']:.2f}% of GDP")
    return result, countries, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar — clear ranking with room for country names
        - **Country selection**: Top 20 by most recent mineral rents % GDP
        - **Year**: Most recent available 2015-2021
        - **Highlights**: DRC at 28.8% is extreme — nearly one third of GDP from minerals.
          Chile leads because of copper; Burkina Faso because of gold.
          Australia's 10.4% shows even a diversified economy can have significant mineral dependence.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
