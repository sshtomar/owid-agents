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
        # Natural Resource Dependency Slope Chart, 2000 vs. 2019 — Methodology

        Slope chart comparing total natural resources rents as % of GDP for
        resource-rich economies at two time points.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-TOTL-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    agg_words = ["World","income","IDA","IBRD","Africa","Asia","Europe","America","Pacific",
                 "dividend","states","Arab","East","Central"]
    by_country = defaultdict(dict)
    for row in data:
        cn = row["countryName"]
        if any(w in cn for w in agg_words):
            continue
        if row["value"] is not None:
            by_country[cn][row["year"]] = row["value"]

    targets = ["Iraq","Congo, Rep.","Angola","Iran, Islamic Rep.","Equatorial Guinea",
               "Azerbaijan","Brunei Darussalam","Chad","Gabon","Algeria","Kazakhstan","Congo, Dem. Rep.","Ghana","Burkina Faso"]
    name_map = {
        "Iran, Islamic Rep.": "Iran", "Equatorial Guinea": "Eq. Guinea",
        "Brunei Darussalam": "Brunei", "Congo, Rep.": "Congo Rep.",
        "Congo, Dem. Rep.": "Congo DR"
    }
    slope = []
    for c in targets:
        yrs = by_country.get(c, {})
        a = yrs.get(2000) or yrs.get(2001)
        b = yrs.get(2019) or yrs.get(2018)
        if a is not None and b is not None:
            slope.append({"n": name_map.get(c, c), "a": round(a, 1), "b": round(b, 1)})
    slope.sort(key=lambda x: -x["a"])
    for s in slope:
        print(f"{s['n']}: {s['a']}% → {s['b']}% ({s['b']-s['a']:+.1f}pp)")
    return slope, by_country, targets, name_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2019) — shows magnitude of change clearly
        - **Country selection**: Resource-rich economies with meaningful 2000 values
        - **Color**: Green for decreasing dependency, orange for increasing (resource curse deepening)
        - **Story**: Most oil/gas exporters saw resource rents shrink as % of GDP (diversification
          or price drops), while Chad, Congo DR, and Burkina Faso saw rents rise as mineral
          extraction expanded
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
