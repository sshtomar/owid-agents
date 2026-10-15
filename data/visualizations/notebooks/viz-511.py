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
        # Suicide Mortality Rate Slope Chart — Methodology

        Slope chart comparing suicide mortality rates (per 100,000 population)
        in 2000 vs 2019 across 25 countries with the largest absolute change.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-SUIC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_terms = ['income', 'World', 'Europe', 'Asia', 'Africa', 'America', 'OECD',
                  'IDA', 'IBRD', 'Pacific', 'Arab', 'Caribbean', 'states', 'region',
                  'countries', 'dividend', 'fragile', 'small', 'East', 'South', 'North',
                  'Central', 'Western', 'Eastern', 'Southern', 'Northern', 'demographic']
    countries = {}
    for row in data:
        c = row['countryName']
        if row['value'] is not None and not any(x.lower() in c.lower() for x in skip_terms):
            if c not in countries:
                countries[c] = {}
            countries[c][row['year']] = row['value']
    good = {c: {'a': v[2000], 'b': v[2019]} for c, v in countries.items() if 2000 in v and 2019 in v}
    print(f"Countries with 2000 and 2019 data: {len(good)}")
    return countries, good


@app.cell
def _(good):
    sorted_by_change = sorted(good.items(), key=lambda x: abs(x[1]['b'] - x[1]['a']), reverse=True)[:25]
    values_a = [v['a'] for _, v in sorted_by_change]
    values_b = [v['b'] for _, v in sorted_by_change]
    print(f"Value range 2000: {min(values_a):.1f} - {max(values_a):.1f}")
    print(f"Value range 2019: {min(values_b):.1f} - {max(values_b):.1f}")
    return sorted_by_change, values_a, values_b


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows before/after at two time points, ideal for comparing direction of change
        - **Country selection**: Top 25 by absolute change; mix of large decreases (Belarus, Hungary) and increases (South Korea, Eswatini)
        - **Color encoding**: Diverging — green for decreasing rates (improvement), orange-red for increasing rates
        - **Time points**: 2000 and 2019 (most recent complete WHO/WB aligned year before COVID)
        - **Story**: Most high-income countries reduced suicide rates; South Korea and Eswatini bucked the trend sharply
        """
    )
    return


@app.cell
def _(json, sorted_by_change):
    chart_data = [
        {"n": "South Korea" if c == "Korea, Rep." else c,
         "a": round(v['a'], 1), "b": round(v['b'], 1)}
        for c, v in sorted_by_change
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
