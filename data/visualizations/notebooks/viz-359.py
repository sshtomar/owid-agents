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
        # Energy Intensity — Methodology

        Horizontal bar chart comparing energy intensity (megajoules of primary energy per
        $2021 PPP GDP) across a cross-section of countries. Lower is better — it means
        more economic output per unit of energy. The chart spans the full range from
        hyper-efficient service economies to energy-heavy industrial and fossil-fuel exporters.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-EGY-PRIM-PP-KD.json"
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
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = round(row["value"], 2)

    skip_keywords = ["World","income","Asia","Africa","Europe","America","Pacific","Arab","OECD",
                     "Caribbean","Central","Eastern","Western","Northern","Sahara","Euro","Latin",
                     "Middle","Small","IDA","IBRD","dividend","fragile","island","developing","Least","developed"]

    countries = {}
    for c, yv in by_country.items():
        if any(k.lower() in c.lower() for k in skip_keywords):
            continue
        recent = {y: v for y, v in yv.items() if 2018 <= y <= 2022}
        if recent and len(yv) >= 10:
            yr = max(recent.keys())
            countries[c] = (yr, recent[yr])

    sorted_c = sorted(countries.items(), key=lambda x: x[1][1], reverse=True)

    major_names = {"Germany", "France", "Japan", "India", "Brazil", "Indonesia", "Argentina", "China"}
    seen = set()
    all_countries = []
    for c, (yr, v) in sorted_c[:8] + [(c, yv) for c, yv in sorted_c if c in major_names] + sorted_c[-5:]:
        if c not in seen:
            seen.add(c)
            all_countries.append({"n": c, "v": v, "y": yr})

    all_countries.sort(key=lambda x: x["v"], reverse=True)
    print(f"Countries in chart: {len(all_countries)}")
    print(f"Range: {min(x['v'] for x in all_countries):.2f} – {max(x['v'] for x in all_countries):.2f} MJ/$ GDP")
    return all_countries, by_country, countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar — clean ranking comparison, room for country names
        - **Country selection**: Top 8 most energy-intensive + major economies for context + bottom 5 most efficient
        - **Year**: Most recent available in 2018-2022 window
        - **Color**: Sequential warm ramp from high to low intensity
        - **Highlights**: China and India are still far more energy-intensive than Western Europe
          despite rapid recent improvements; Ireland and Hong Kong lead efficiency
        """
    )
    return


@app.cell
def _(json, all_countries):
    print(json.dumps(all_countries, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
