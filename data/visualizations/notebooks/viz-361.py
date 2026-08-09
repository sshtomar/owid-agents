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
        # Preprimary School Enrollment -- Methodology

        Slope chart comparing gross preprimary enrollment rate (1999 vs 2019) for
        16 countries. World Bank indicator SE.PRE.ENRR.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRE-ENRR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    priority = ['Ghana', 'Iran, Islamic Rep.', 'Georgia', 'Costa Rica', 'China',
                'Kazakhstan', 'Finland', 'Bhutan', 'Ethiopia', 'Albania', 'Bolivia',
                'Kenya', 'Cameroon', 'Jordan', 'Djibouti', 'Burkina Faso']
    filtered = [r for r in data if r["value"] is not None and r["countryName"] in priority and r["year"] in (1999, 2019)]
    print(f"Filtered to {len(filtered)} rows for priority countries in 1999 and 2019")
    return (filtered,)


@app.cell
def _(filtered):
    by_country = {}
    for r in filtered:
        if r["countryName"] not in by_country:
            by_country[r["countryName"]] = {}
        by_country[r["countryName"]][r["year"]] = r["value"]
    pairs = [(name, v[1999], v[2019]) for name, v in by_country.items() if 1999 in v and 2019 in v]
    print(f"Countries with 1999 and 2019 data: {len(pairs)}")
    for name, a, b in sorted(pairs, key=lambda x: x[2]):
        print(f"  {name}: {a:.1f}% -> {b:.1f}% ({b-a:+.1f})")
    return (pairs,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- two-point comparison, 1999-2019
        - **Country selection**: Mix of big gainers (Iran, Georgia, Ghana) and laggards (Burkina Faso, Djibouti)
        - **Gross enrollment**: Can exceed 100% due to age overlap and late entrants
        - **Color**: Warmer = bigger absolute gain
        """
    )
    return


@app.cell
def _(json, pairs):
    chart_data = [
        {"n": name.replace(", Islamic Rep.", "").replace(", Arab Rep.", ""),
         "a": round(a, 1), "b": round(b, 1)}
        for name, a, b in sorted(pairs, key=lambda x: x[2])
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
