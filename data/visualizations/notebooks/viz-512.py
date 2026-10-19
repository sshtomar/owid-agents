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
        # Learning-Adjusted Years of School — Methodology

        Documents the data pipeline behind viz-512: slope chart comparing
        2010 vs 2020 learning-adjusted years of school across 22 countries
        spanning the full quality spectrum.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--HD-HCI-LAYS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    non_null = [r for r in data if r["value"] is not None]
    skip_kw = ["World","income","Africa","Asia","Pacific","Europe","America",
               "Caribbean","Arab","OECD","Union","states","countries","Latin",
               "Middle East","North America","South Asia","Sub-Saharan","Fragility",
               "Euro area","Central Europe","East Asia"]

    def is_region(n):
        return any(k.lower() in n.lower() for k in skip_kw)

    real = [r for r in non_null if not is_region(r["countryName"])]
    y2010 = {r["countryName"]: round(r["value"], 1) for r in real if r["year"] == 2010}
    y2020 = {r["countryName"]: round(r["value"], 1) for r in real if r["year"] == 2020}
    both = [(n, y2010[n], y2020[n]) for n in y2020 if n in y2010]
    both_sorted = sorted(both, key=lambda x: -x[2])

    print(f"Countries with both 2010 and 2020: {len(both_sorted)}")
    print(f"Value range (2020): {both_sorted[-1][2]:.1f} – {both_sorted[0][2]:.1f}")
    return both, both_sorted, non_null, real, y2010, y2020


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows 2010→2020 change in education quality
          for 22 diverse countries, revealing which systems improved and which stagnated
        - **Country selection**: Top 7 (Singapore–Canada), 5 mid-range, bottom 10
          to capture the full spectrum from Singapore (12.8 years) to Chad (2.8 years)
        - **Notable findings**:
          - Finland and Japan show slight declines (−0.5, −0.3 years) over the decade
          - Burkina Faso gained the most (+1.3 years, 41% improvement)
          - Chad unchanged at 2.8 — the lowest in the dataset
          - Singapore leads at 12.8 learning-adjusted years despite typical schooling
            of 14+ years (quality-adjusted school completion)
        """
    )
    return


@app.cell
def _(json, both_sorted):
    selected = [
        {"n": n, "a": a, "b": b}
        for n, a, b in both_sorted
        if n in [
            "Singapore","Finland","Japan","Canada","Estonia","New Zealand","Norway",
            "Cyprus","Spain","Serbia","Kazakhstan","Qatar","Uruguay","Brazil",
            "Zimbabwe","Namibia","Burundi","Madagascar","Burkina Faso","Eswatini",
            "Uganda","Chad"
        ]
    ]
    print(json.dumps(selected, separators=(",", ":")))
    return (selected,)


if __name__ == "__main__":
    app.run()
