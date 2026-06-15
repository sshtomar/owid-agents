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
        # Old-Age Dependency Ratio — Methodology

        Slope chart comparing old-age dependency ratios in 1970 vs 2023
        across 21 countries. Highlights the extreme aging of Japan and
        Eastern Europe versus stable young-age structures in Sub-Saharan Africa.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregates = {
        'Africa Eastern and Southern','Africa Western and Central','Arab World',
        'Caribbean small states','Central Europe and the Baltics','East Asia & Pacific',
        'Euro area','Europe & Central Asia','European Union','High income','IBRD only',
        'IDA & IBRD total','IDA blend','IDA only','IDA total','Latin America & Caribbean',
        'Least developed countries: UN classification','Low & middle income','Low income',
        'Lower middle income','Middle East & North Africa','Middle income','North America',
        'Not classified','OECD members','Other small states','Pacific island small states',
        'South Asia','Sub-Saharan Africa','Upper middle income','West Bank and Gaza','World',
        'Early-demographic dividend','Late-demographic dividend','Post-demographic dividend',
        'Pre-demographic dividend','Small states','Isle of Man','Channel Islands','Bermuda',
        'Gibraltar','Kosovo','Curacao'
    }
    pts = {}
    for p in data:
        cn = p['countryName']
        if cn in aggregates or p['value'] is None:
            continue
        pts.setdefault(cn, {})[p['year']] = p['value']

    both = {
        cn: (pts[cn][1970], pts[cn][2023])
        for cn in pts
        if 1970 in pts[cn] and 2023 in pts[cn]
    }
    print(f"Countries with both 1970 and 2023: {len(both)}")
    return aggregates, both, pts


@app.cell
def _(both):
    sorted_2023 = sorted(both.items(), key=lambda x: x[1][1], reverse=True)
    top_aging = sorted_2023[:12]
    by_change = sorted(both.items(), key=lambda x: x[1][1] - x[1][0], reverse=True)
    rising = [(cn, v) for cn, v in by_change if cn not in dict(top_aging)][:8]
    lowest = sorted_2023[-8:]

    selected = {}
    for cn, (a, b) in top_aging + rising + lowest:
        selected[cn] = (a, b)

    chart_data = [
        {"n": cn, "a": round(a, 1), "b": round(b, 1)}
        for cn, (a, b) in sorted(selected.items(), key=lambda x: x[1][1], reverse=True)[:26]
    ]
    print(f"Final dataset: {len(chart_data)} countries")
    for row in chart_data[:5]:
        print(f"  {row['n']}: {row['a']} -> {row['b']}")
    return chart_data, lowest, rising, selected, sorted_2023, top_aging


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — best for showing directional change between two time points
        - **Country selection**: Top 12 by 2023 ratio (aging crisis cases), 8 fastest-rising, 8 lowest
        - **Time range**: 1970–2023 — captures the full demographic transition era
        - **Color**: Warm tones = large increase; cool = stable/decline
        - **Highlights**: Japan sextupled its ratio; Sub-Saharan Africa barely changed
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
