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
        # Exclusive Breastfeeding Rates — Methodology

        Horizontal bar chart ranking countries by most recent exclusive breastfeeding
        rate (% of infants under 6 months), showing wide global variation.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-BFED-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    agg_words = ["World","income","IDA","IBRD","Africa","Asia","Europe","America","Pacific",
                 "dividend","states","Arab","East","Central","South","Sub-","region","total","Least"]
    by_country = defaultdict(list)
    for row in data:
        cn = row["countryName"]
        if any(w in cn for w in agg_words):
            continue
        if row["value"] is not None and row["year"] >= 2011:
            by_country[cn].append((row["year"], row["value"]))

    recent = {}
    for c, vals in by_country.items():
        sv = sorted(vals, key=lambda x: x[0])
        recent[c] = sv[-1]

    sorted_c = sorted(recent.items(), key=lambda x: -x[1][1])
    print(f"Countries with data from 2011+: {len(sorted_c)}")
    for c, (y, v) in sorted_c[:25]:
        print(f"  {c} ({y}): {v:.1f}%")
    return by_country, recent, sorted_c


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — easy country comparison at a single point
        - **Country selection**: Top high-rate countries plus a few low-rate countries for contrast
        - **Color**: Green for rates ≥60%, lighter green for 45–60%, amber for 25–45%, orange for <25%
        - **Story**: Sub-Saharan Africa and South Asia achieve 55–72% exclusive breastfeeding;
          some Latin American and Eastern European countries fall below 20%
        - **Note**: Survey years vary by country (2012–2020); this reflects most recent data available
        """
    )
    return


@app.cell
def _(json):
    chart_data = [
        {"n":"Burundi",       "v":71.9,"y":2019},
        {"n":"N. Korea",      "v":71.4,"y":2017},
        {"n":"Cambodia",      "v":65.2,"y":2014},
        {"n":"Eswatini",      "v":63.8,"y":2014},
        {"n":"Kiribati",      "v":63.6,"y":2019},
        {"n":"Bangladesh",    "v":62.6,"y":2019},
        {"n":"Kenya",         "v":61.4,"y":2014},
        {"n":"Guinea-Bissau", "v":59.3,"y":2019},
        {"n":"Ethiopia",      "v":58.8,"y":2019},
        {"n":"India",         "v":58.0,"y":2018},
        {"n":"Burkina Faso",  "v":57.9,"y":2019},
        {"n":"Afghanistan",   "v":57.5,"y":2018},
        {"n":"Bolivia",       "v":55.7,"y":2016},
        {"n":"Gambia",        "v":53.6,"y":2020},
        {"n":"Congo DR",      "v":53.6,"y":2018},
        {"n":"Indonesia",     "v":50.7,"y":2017},
        {"n":"El Salvador",   "v":46.7,"y":2014},
        {"n":"Georgia",       "v":20.4,"y":2018},
        {"n":"Bosnia & Herz.","v":18.2,"y":2012},
        {"n":"Dominican Rep.","v": 4.6,"y":2014},
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
