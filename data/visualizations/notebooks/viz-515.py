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
        # Urban Safe Drinking Water -- Methodology

        Slope chart comparing share of urban population with safely managed
        drinking water access in 2000 vs. latest available year (2018+).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-H2O-SMDW-UR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SKIP = [
        "IDA","IBRD","income","Sub-","Asia Pacific","Europe","Pacific","America",
        "World","dividend","blend","Euro area","OECD","Arab World","Middle East",
        "Caribbean","Fragility","Conflict","Violence","Least developed","Heavily",
        "HIPC","South Asia","countries:","small states","Saharan","Eastern","Western",
        "Central","Northern","Organisation","only","Late-","Pre-","Early-",
        "Upper","Lower","High income","Low income","IDA & IBRD","excluding high",
        "Africa Eastern","Africa Western","East Asia","&"
    ]
    def is_country(row):
        name = row["countryName"]
        return not any(kw in name for kw in SKIP)

    NAME_MAP = {
        "Congo, Dem. Rep.": "DR Congo",
        "Gambia, The": "Gambia",
        "Iran, Islamic Rep.": "Iran",
    }

    country_data = [r for r in data if is_country(r)]
    country_years = {}
    for r in country_data:
        c = r["countryName"]
        if c not in country_years:
            country_years[c] = {}
        if r["value"] is not None:
            country_years[c][r["year"]] = r["value"]
    print(f"Country-level: {len(country_years)} countries")
    return NAME_MAP, country_years, country_data, is_country


@app.cell
def _(NAME_MAP, country_years, json):
    SELECTED = [
        "Chad","Afghanistan","Congo, Dem. Rep.","Ethiopia",
        "Ghana","Bangladesh","Gambia, The","Honduras","Cambodia",
        "Guatemala","India","Iraq","Brazil","Georgia",
        "Botswana","Algeria","El Salvador",
        "China","France","Germany"
    ]

    result = []
    for country in SELECTED:
        yd = country_years.get(country, {})
        if 2000 in yd:
            recent = {y: v for y, v in yd.items() if y >= 2018}
            if recent:
                b_yr = max(recent.keys())
                result.append({
                    "n": NAME_MAP.get(country, country),
                    "a": round(yd[2000], 1),
                    "b": round(recent[b_yr], 1),
                })

    result.sort(key=lambda x: x["a"])
    for r in result:
        print(f"  {r['n']}: {r['a']}% -> {r['b']}% ({r['b']-r['a']:+.1f} pp)")
    print()
    print("JSON:")
    print(json.dumps(result, separators=(",", ":")))
    return (result,)


if __name__ == "__main__":
    app.run()
