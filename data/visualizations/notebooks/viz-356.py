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
        # Safely Managed Drinking Water — Methodology

        Slope chart comparing the share of population with safely managed drinking water
        in 2000 vs 2022 for 22 countries. "Safely managed" means: on premises, available
        when needed, free from contamination. Much stricter than "basic access."
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-H2O-SMDW-ZS.json"
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
        'Gibraltar','Kosovo','Curacao','Sint Maarten (Dutch part)'
    }
    pts = {}
    for p in data:
        cn = p['countryName']
        if cn in agg or p['value'] is None:
            continue
        pts.setdefault(cn, {})[p['year']] = p['value']

    both = {
        cn: (pts[cn][2000], pts[cn][2022])
        for cn in pts
        if 2000 in pts[cn] and 2022 in pts[cn]
    }
    print(f"Countries with 2000 and 2022: {len(both)}")
    return agg, both, pts


@app.cell
def _(both):
    sorted_b = sorted(both.items(), key=lambda x: x[1][1])
    lowest = sorted_b[:12]
    by_gain = sorted(both.items(), key=lambda x: x[1][1] - x[1][0], reverse=True)
    big_gainers = [(cn, v) for cn, v in by_gain if cn not in dict(lowest)][:8]
    specials = [
        (cn, both[cn]) for cn in ['India','China','Brazil','Indonesia','Bangladesh','Jordan']
        if cn in both and cn not in dict(lowest) and cn not in dict(big_gainers)
    ]

    selected = {cn: (a, b) for cn, (a, b) in lowest + big_gainers + specials if abs(b-a) > 0.5 or b < 50}
    chart_data = [
        {"n": cn, "a": round(a, 1), "b": round(b, 1)}
        for cn, (a, b) in sorted(selected.items(), key=lambda x: x[1][1])[:24]
    ]
    print(f"Final dataset: {len(chart_data)} countries")
    for row in chart_data[:5]:
        print(f"  {row['n']}: {row['a']}% -> {row['b']}%")
    return big_gainers, chart_data, lowest, selected, sorted_b, specials


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — directional comparison across two time points
        - **Country selection**: Lowest-access countries + biggest improvers + key populous nations
        - **Time range**: 2000–2022 (SDG monitoring era)
        - **Color**: Warm = large improvement; cool = stagnant or declined
        - **Highlights**: India gained 35pp; Chad still at 6%; Jordan jumped 30pp
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
