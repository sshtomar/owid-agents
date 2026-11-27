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

        Slope chart comparing 1990 vs 2023 lifetime risk of dying from maternal
        causes for the 20 highest-burden countries. Shows dramatic progress in
        most, with Chad and Central African Republic as outliers.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MMR-RISK-ZS.json"
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

    yr1990, yr2023 = {}, {}
    for row in data:
        cn = row['countryName']
        if row['value'] is None or is_agg(cn):
            continue
        if row['year'] == 1990:
            yr1990[cn] = round(row['value'], 3)
        elif row['year'] == 2023:
            yr2023[cn] = round(row['value'], 3)

    both = [(cn, yr1990[cn], yr2023[cn]) for cn in yr1990 if cn in yr2023]
    ranked = sorted(both, key=lambda x: -x[1])
    print(f"Countries with both years: {len(both)}")
    for cn, a, b in ranked[:5]:
        print(f"  {cn}: {a:.2f}% → {b:.2f}%")
    return both, is_agg, ranked, yr1990, yr2023


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — directly shows before/after change per country
        - **Country selection**: Top 20 by 1990 risk (all high-burden individual countries)
        - **Color**: Encodes % reduction — green for large drops, red for minimal progress
        - **Highlights**: Bangladesh −94%, Ethiopia −91%; Chad still 4.2%, C.A.R. 4.2%
        """
    )
    return


@app.cell
def _(json, ranked):
    top20 = [(cn.replace(', The', '').replace(', Dem. Rep.', ''), a, b) for cn, a, b in ranked[:20]]
    chart_data = [{"n": cn, "a": a, "b": b} for cn, a, b in top20]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
