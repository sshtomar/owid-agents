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
    # Premature NCD Mortality — Methodology

    Slope chart showing probability (%) of dying between ages 30 and 70 from cardiovascular
    disease, cancer, diabetes, or chronic respiratory disease — 2000 vs 2021.
    Countries with highest 2000 values shown. Color encodes improvement magnitude.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-NCOM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} points")
    return data, raw


@app.cell
def _(data, json):
    points = [r for r in data if r["value"] is not None]
    exclude_terms = ["World","Income","OECD","Arab World","Africa ","Asia ","Europe ","America","Caribbean",
                     "dividend","heavily","Fragile","IDA","IBRD","Euro area","Latin ","Sub-Saharan","South Asia",
                     "East Asia","Pacific","Central Asia","Middle East","North Africa","MENA","classification","states"]
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
        v2000 = yd.get(2000)
        v2021 = yd.get(2021)
        if v2000 is not None and v2021 is not None:
            slope_data.append({"n": c, "a": round(v2000, 1), "b": round(v2021, 1)})

    slope_data.sort(key=lambda x: -x["a"])
    top30 = slope_data[:30]
    print(f"Top 30 countries by 2000 NCD mortality:")
    for t in top30:
        print(f"  {t['n']}: {t['a']} -> {t['b']} ({t['b']-t['a']:+.1f})")
    print(json.dumps(top30, separators=(",", ":")))
    return (top30,)


if __name__ == "__main__":
    app.run()
