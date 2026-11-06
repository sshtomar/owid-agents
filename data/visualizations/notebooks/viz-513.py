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
        # Primary School Enrollment Progress -- Methodology

        Shows how low-enrollment countries dramatically expanded primary
        school access from roughly 2000 to 2017, using the adjusted net
        enrollment rate (% of primary-age children).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-TENR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x["value"] is not None:
            by_country[x["countryName"]][x["year"]] = round(x["value"], 1)

    skip_patterns = ["income", "HIPC", "classified", "dividend", "IDA", "IBRD",
                     "region", "Europe", "East Asia", "Americas", "Caribbean",
                     "South Asia", "Africa", "developed", "developing", "fragile",
                     "small state", "Euro", "World", "Central America", "Latin"]

    slope_data = []
    for c, ymap in by_country.items():
        if any(p.lower() in c.lower() for p in skip_patterns):
            continue
        early_years = [y for y in range(2000, 2007) if y in ymap]
        late_years = [y for y in range(2015, 2020) if y in ymap]
        if early_years and late_years:
            early = ymap[max(early_years)]
            late = ymap[max(late_years)]
            if early < 90 and late > early:
                slope_data.append({"n": c, "a": early, "b": late, "diff": late - early})

    slope_data.sort(key=lambda x: x["diff"], reverse=True)
    print(f"Countries with significant gains: {len(slope_data)}")
    for s in slope_data[:15]:
        print(f"  {s['n']}: {s['a']} -> {s['b']} (+{s['diff']:.1f}pp)")
    return (slope_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows change between two time points clearly
        - **Country selection**: Countries starting below 90% enrollment with measurable
          progress from ~2000 to ~2017; focus on sub-Saharan Africa and South Asia
        - **Time range**: ~2000 to ~2017 -- captures the MDG primary education push
        - **Color**: Warmer for larger gains, cooler for smaller gains
        - **Story**: Ivory Coast went from 56% to 94% -- most children now in school
          who weren't 17 years earlier. Eritrea is a rare case of regression.
        """
    )
    return


@app.cell
def _(json, slope_data):
    chart_data = []
    name_map = {"Cote d'Ivoire": "Ivory Coast", "Gambia, The": "Gambia"}
    for s in slope_data:
        n = name_map.get(s["n"], s["n"])
        chart_data.append({"n": n, "a": s["a"], "b": s["b"]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
