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
        # Educated Unemployment -- Methodology

        Slope chart comparing unemployment rates among workers with
        advanced education, mid 2000s vs. late 2010s. Reveals where
        credential inflation or economic mismatch is worsening.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-UEM-ADVN-ZS.json"
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
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Bosnia and Herzegovina": "Bosnia & Herz.",
    }

    country_data = [r for r in data if is_country(r)]
    country_years = {}
    for r in country_data:
        c = r["countryName"]
        if c not in country_years:
            country_years[c] = {}
        if r["value"] is not None:
            country_years[c][r["year"]] = r["value"]
    print(f"Country-level entries: {len(country_years)}")
    return NAME_MAP, country_years, country_data, is_country


@app.cell
def _(NAME_MAP, country_years, json):
    early_window = (2005, 2010)
    recent_window = (2018, 2024)

    SELECTED = [
        "Angola","Botswana","Iraq","Cameroon","Bangladesh",
        "India","Burkina Faso","Ethiopia",
        "Egypt, Arab Rep.","Armenia","Bosnia and Herzegovina",
        "Albania","Indonesia","Iran, Islamic Rep.","Kenya",
        "Colombia","Greece","Ireland","Chile","Japan"
    ]

    result = []
    for country in SELECTED:
        yd = country_years.get(country, {})
        early = {y: v for y, v in yd.items() if early_window[0] <= y <= early_window[1]}
        recent = {y: v for y, v in yd.items() if recent_window[0] <= y <= recent_window[1]}
        if early and recent:
            a_yr = max(early.keys())
            b_yr = max(recent.keys())
            result.append({
                "n": NAME_MAP.get(country, country),
                "a": round(early[a_yr], 1),
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
