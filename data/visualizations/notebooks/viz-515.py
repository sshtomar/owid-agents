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
        # Anemia in Pregnant Women — Methodology

        Slope chart comparing anemia prevalence in 2000 vs 2023 for the 20
        highest-burden countries. Persistent problem in West Africa and South Asia.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-PRG-ANEM.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregate_patterns = [
        'income', 'World', '& Pacific', '& Central', 'Middle East',
        'Latin America', 'Sub-Saharan', 'North Africa', 'Euro area', 'South Asia',
        'East Asia', 'Arab World', 'Caribbean small', 'OECD', 'fragile', 'Fragility',
        'IDA', 'IBRD', 'island', 'Small states', 'Heavily', 'Least',
        'demographic', 'Africa Western', 'Africa Eastern', 'Europe &'
    ]
    def is_agg(cn):
        return any(x.lower() in cn.lower() for x in aggregate_patterns)

    yr2000, yr2023 = {}, {}
    for row in data:
        cn = row['countryName']
        if row['value'] is None or is_agg(cn):
            continue
        if row['year'] == 2000:
            yr2000[cn] = round(row['value'], 1)
        elif row['year'] == 2023:
            yr2023[cn] = round(row['value'], 1)

    both = [(cn, yr2000[cn], yr2023[cn]) for cn in yr2000 if cn in yr2023]
    ranked = sorted(both, key=lambda x: -x[1])
    print(f"Countries with both years: {len(both)}")
    for cn, a, b in ranked[:5]:
        print(f"  {cn}: {a:.0f}% → {b:.0f}%")
    return both, is_agg, ranked, yr2000, yr2023


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — before/after change per country
        - **Country selection**: Top 20 by 2000 prevalence (highest burden)
        - **Color**: Encodes % reduction (darker green = more improvement)
        - **Highlights**: Cambodia −27%; Côte d'Ivoire almost unchanged at 57%; West Africa cluster above 50%
        """
    )
    return


@app.cell
def _(json, ranked):
    top20 = []
    for cn, a, b in ranked[:20]:
        label = cn.replace(', Rep.', '').replace(', Dem. Rep.', ' D.R.')
        top20.append({"n": label, "a": a, "b": b})
    print(json.dumps(top20, separators=(",", ":")))
    return (top20,)


if __name__ == "__main__":
    app.run()
