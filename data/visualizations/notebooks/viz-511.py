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
        # Lifetime Risk of Maternal Death — Methodology

        Documents the data pipeline behind viz-511: slope chart comparing
        1990 vs 2023 lifetime maternal death risk per 1,000 women across
        14 high-burden countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MMR-RISK.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    non_null = [r for r in data if r["value"] is not None]

    def is_region(name):
        kw = ["income","africa","asia","pacific","europe","america","caribbean",
              "world","Arab","OECD","Union","dividend","HIPC","IDA","states",
              "countries","Central Europe","East Asia","Euro area","Latin",
              "Middle East","North America","South Asia","Sub-Saharan","Fragility"]
        return any(k.lower() in name.lower() for k in kw)

    real = [r for r in non_null if not is_region(r["countryName"])]
    y1990 = {r["countryName"]: r["value"] for r in real if r["year"] == 1990}
    y2023 = {r["countryName"]: r["value"] for r in real if r["year"] == 2023}
    both = [(n, y1990[n], y2023[n]) for n in y2023 if n in y1990]
    # Convert to risk per 1,000 women
    risk_data = sorted(
        [(n, round(1000/a, 1), round(1000/b, 1)) for n, a, b in both],
        key=lambda x: -x[1]
    )
    print(f"Countries with both 1990 and 2023: {len(risk_data)}")
    print("Top 16 by 1990 risk (per 1,000 women):")
    for n, a, b in risk_data[:16]:
        pct = round((a - b) / a * 100)
        print(f"  {n}: {a} -> {b} ({pct}% reduction)")
    return both, non_null, real, risk_data, y1990, y2023


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for comparing two time points (1990 vs 2023)
          across many entities, with lines visually encoding direction and magnitude of change
        - **Country selection**: Top 14 highest-risk countries in 1990 (excluding aggregate
          regions), focusing on Sub-Saharan Africa and South/Southeast Asia where most
          maternal deaths occur
        - **Unit conversion**: Raw "1 in X" format converted to "deaths per 1,000 women"
          for intuitive reading (higher = more dangerous)
        - **Color encoding**: Diverging ramp by % reduction achieved; countries that have
          made the least progress (Chad, Central African Republic) shown in terra red
        - **Highlights**:
          - Bangladesh: 94% reduction (41.7 → 2.6 per 1,000)
          - Ethiopia: 91% reduction (83.3 → 7.9 per 1,000)
          - Chad and Central African Republic: stuck above 40 per 1,000
        """
    )
    return


@app.cell
def _(json, risk_data):
    selected_countries = [
        "Afghanistan","Guinea-Bissau","Burundi","Ethiopia","Chad","Gambia, The",
        "Eritrea","Guinea","Angola","Central African Republic","Burkina Faso",
        "Comoros","Bangladesh","Cambodia"
    ]
    name_remap = {"Gambia, The": "Gambia", "Central African Republic": "Central African Rep."}

    chart_data = [
        {"n": name_remap.get(n, n), "a": a, "b": b}
        for n, a, b in risk_data
        if n in selected_countries
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, name_remap, selected_countries


if __name__ == "__main__":
    app.run()
