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
    mo.md("""
    # Intentional Homicides — Methodology

    Slope chart comparing homicide rates around 2000 vs. most recent year for the 25 countries
    with the highest current rates. Shows Latin America's dominant presence and diverging trends.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} points")
    return data, raw


@app.cell
def _(data, json):
    points = [r for r in data if r["value"] is not None]
    exclude_terms = ["World","Income","OECD","Arab World","Africa ","Asia ","Europe ","America","Caribbean",
                     "dividend","heavily","Fragile","IDA","IBRD","Euro area","Latin ","Sub-Saharan","South Asia",
                     "East Asia","Pacific","Central Asia","Middle East","North Africa","MENA","states"]
    def is_real_country(name):
        return not any(x.lower() in name.lower() for x in exclude_terms)
    real_pts = [r for r in points if is_real_country(r["countryName"])]

    by_country = {}
    for r in real_pts:
        c = r["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][r["year"]] = r["value"]

    slope_data = []
    for c, yd in by_country.items():
        v2000 = None
        for y in [2000, 2001, 1999, 2002]:
            if y in yd:
                v2000 = yd[y]
                break
        recent_year = max(yd.keys())
        v_recent = yd[recent_year]
        if v2000 is not None:
            slope_data.append({"n": c, "a": round(v2000, 1), "b": round(v_recent, 1)})

    slope_data.sort(key=lambda x: -x["b"])
    top25 = slope_data[:25]
    print(f"Top 25 by current rate:")
    for t in top25:
        print(f"  {t['n']}: {t['a']} -> {t['b']}")
    print(json.dumps(top25, separators=(",", ":")))
    return (top25,)


if __name__ == "__main__":
    app.run()
