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
        # Primary School Completion Rate — Methodology

        Slope chart comparing primary school completion rates around 2000 vs. around 2022
        for 17 countries spanning the full range from Chad (~22%) to Indonesia (~100%).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_kw = ['income','region','world','small states','fragile','developing','IBRD','IDA','OECD',
               'Pacific','Africa','Asia','Caribbean','Americas','Arab','Saharan','Central','South',
               'North','East','West','Latin','Europe','dividend','blend','states','average','total',
               'excluding','G7','G20','HIPC']
    def is_agg(cn):
        return any(kw.lower() in cn.lower() for kw in skip_kw)

    countries = {}
    for row in data:
        cn = row["countryName"]
        if is_agg(cn) or row["value"] is None:
            continue
        if cn not in countries:
            countries[cn] = {}
        countries[cn][row["year"]] = row["value"]

    print(f"Individual countries: {len(countries)}")
    return countries, is_agg


@app.cell
def _(countries):
    def nearest_year(d, target, tol=5):
        for offset in range(tol + 1):
            for delta in [0, offset, -offset]:
                y = target + delta
                if y in d and d[y] is not None:
                    return y, d[y]
        return None, None

    selected = [
        "Chad", "Burundi", "Burkina Faso", "Benin", "Guinea",
        "Cote d'Ivoire", "Ethiopia", "Comoros", "Congo, Rep.", "Cameroon",
        "Honduras", "Cambodia", "Guatemala", "Indonesia", "Colombia",
        "India", "Jordan"
    ]

    chart_data = []
    for cn in selected:
        if cn not in countries:
            print(f"NOT FOUND: {cn}")
            continue
        cd = countries[cn]
        _, vb = nearest_year(cd, 2000, 3)
        _, va = nearest_year(cd, 2022, 3)
        if vb is None or va is None:
            print(f"MISSING DATA: {cn}")
            continue
        chart_data.append({"n": cn, "a": round(min(vb, 100.0), 1), "b": round(min(va, 100.0), 1)})
        print(f"{cn}: {vb:.1f} -> {va:.1f}")

    print(f"\nTotal: {len(chart_data)} countries")
    return chart_data, nearest_year, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — perfect for comparing exactly two time points across
          many entities; the direction and angle of each line tells the story immediately
        - **Country selection**: Covers the full range from ~20% (Chad, 2000) to ~100%
          (Indonesia, Jordan), weighted toward Sub-Saharan Africa where the gap is widest
        - **Year pairing**: ~2000 (using nearest available year within ±3) vs. ~2022
        - **Capping**: Values above 100% are capped at 100 (GER > 100 reflects late entrants
          and age mismatches in gross enrollment statistics)
        - **Color**: Encodes magnitude of change — deep green for 30+ point gains, amber for
          modest gains, red for declines
        - **Highlights**: Ethiopia gained 39 points; Cambodia 37; Chad gained only 20 points
          and remains the lowest in the set at 42%
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
