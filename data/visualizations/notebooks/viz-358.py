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
    # Anemia Among Women of Reproductive Age — Methodology

    Documents the data pipeline behind viz-358.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-ALLW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    exclude_words = ["income", "World", "Africa", "Europe", "America", "Pacific",
                     "Caribbean", "Arab", "Euro", "Central", "East", "South", "North",
                     "Sub-Saharan", "Middle", "Least", "dividend", "fragile", "HIPC",
                     "IBRD", "IDA", "OECD", "states", "Heavily", "region"]
    countries_pts = [d for d in filtered if not any(e in d["countryName"] for e in exclude_words)]
    print(f"After filtering aggregates: {len(countries_pts)} rows")
    return countries_pts, exclude_words, filtered


@app.cell
def _(countries_pts):
    by_country = {}
    for d in countries_pts:
        c = d["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][d["year"]] = d["value"]

    valid = {c: v for c, v in by_country.items() if 2000 in v and 2023 in v}
    ranked = sorted(valid.items(), key=lambda x: x[1][2023], reverse=True)
    print(f"Countries with 2000+2023 data: {len(valid)}")
    print(f"Top 5 by 2023: {[(n, round(v[2023],1)) for n, v in ranked[:5]]}")
    return by_country, ranked, valid


@app.cell
def _(mo):
    mo.md("""
    ## Design Rationale

    - **Chart type**: Slope chart — compares two time points across many countries
    - **Country selection**: Top 17 countries by 2023 prevalence (all >38%)
    - **Time range**: 2000 vs 2023 (full 23-year span available)
    - **Highlights**: India is the outlier — prevalence rose from 50% to 54%. Most West African countries improved but remain very high. Afghanistan worsened dramatically (+14pp).
    """)
    return


@app.cell
def _(json, ranked):
    name_fixes = {"Gambia, The": "Gambia", "Congo, Dem. Rep.": "Congo, D.R."}
    chart_data = []
    for name, vals in ranked[:17]:
        display_name = name_fixes.get(name, name)
        chart_data.append({"n": display_name, "a": round(vals[2000], 1), "b": round(vals[2023], 1)})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
