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
        # Adult Female Mortality Rate — Methodology

        Slope chart comparing adult female mortality (deaths per 1,000 women aged 15-60)
        between 1990 and 2020 for 22 high-burden countries. Most made large gains;
        Central African Republic deteriorated.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-AMRT-FE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg = {
        'Africa Eastern and Southern','Africa Western and Central','Arab World',
        'Caribbean small states','Central Europe and the Baltics','East Asia & Pacific',
        'East Asia & Pacific (excluding high income)','East Asia and Pacific (IDA & IBRD countries)',
        'Euro area','Europe & Central Asia','Europe & Central Asia (IDA & IBRD countries)',
        'Europe & Central Asia (excluding high income)','European Union',
        'Fragile and conflict affected situations','Heavily indebted poor countries (HIPC)',
        'High income','IBRD only','IDA & IBRD total','IDA blend','IDA only','IDA total',
        'Late-demographic dividend','Early-demographic dividend','Latin America & Caribbean',
        'Latin America & Caribbean (excluding high income)',
        'Latin America and the Caribbean (IDA & IBRD countries)',
        'Least developed countries: UN classification','Low & middle income','Low income',
        'Lower middle income','Middle East & North Africa',
        'Middle East & North Africa (excluding high income)',
        'Middle East & North Africa (IDA & IBRD countries)','Middle income','North America',
        'Not classified','OECD members','Other small states','Pacific island small states',
        'Post-demographic dividend','Pre-demographic dividend','Small states','South Asia',
        'South Asia (IDA & IBRD)','Sub-Saharan Africa',
        'Sub-Saharan Africa (IDA & IBRD countries)',
        'Sub-Saharan Africa (excluding high income)','Upper middle income',
        'West Bank and Gaza','World','Isle of Man','Channel Islands','Bermuda',
        'Gibraltar','Andorra','Monaco','San Marino'
    }
    pts = {}
    for p in data:
        cn = p['countryName']
        if cn in agg or p['value'] is None:
            continue
        pts.setdefault(cn, {})[p['year']] = p['value']

    both = {
        cn: (pts[cn][1990], pts[cn][2020])
        for cn in pts
        if 1990 in pts[cn] and 2020 in pts[cn]
    }
    print(f"Countries with 1990 and 2020: {len(both)}")
    return agg, both, pts


@app.cell
def _(both):
    sorted_1990 = sorted(both.items(), key=lambda x: x[1][0], reverse=True)
    top15 = sorted_1990[:15]

    specials = [
        cn for cn in ['China','India','Brazil','Mexico','Indonesia','Bangladesh','Pakistan']
        if cn in both and cn not in dict(top15)
    ]

    selected = {cn: both[cn] for cn, _ in top15}
    for cn in specials:
        selected[cn] = both[cn]

    chart_data = [
        {"n": cn, "a": round(a, 0), "b": round(b, 0)}
        for cn, (a, b) in sorted(selected.items(), key=lambda x: x[1][0], reverse=True)[:22]
    ]
    print(f"Final dataset: {len(chart_data)} countries")
    for row in chart_data[:5]:
        pct = (row['a'] - row['b']) / row['a'] * 100
        print(f"  {row['n']}: {row['a']} -> {row['b']} ({pct:+.0f}%)")
    return chart_data, selected, specials, sorted_1990, top15


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows directional change between two time points
        - **Country selection**: Top 15 by 1990 mortality + 7 populous developing countries
        - **Time range**: 1990–2020 — captures three decades of health improvement
        - **Color**: Green shades = large decline; amber = moderate; deep red = worsened
        - **Highlights**: Ethiopia cut mortality 58%; Central African Republic rose 14%
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
