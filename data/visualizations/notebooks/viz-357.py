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
        # International Tourism Arrivals — Methodology

        Documents the data pipeline behind viz-357.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_words = [
        'Africa', 'Asia', 'Europe', 'America', 'Caribbean', 'Pacific',
        'Middle East', 'World', 'OECD', 'IDA', 'IBRD', 'income', 'states',
        'dividend', 'Euro', 'Arab', 'South Asia', 'Latin', 'Sub-Saharan',
        'Least developed', 'Heavily', 'HIPC', 'Channel', 'Islands'
    ]
    filtered = [
        x for x in data
        if x['value'] is not None and not any(w in x['countryName'] for w in exclude_words)
    ]
    print(f"After filtering aggregates: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in filtered:
        by_country[x['countryName']][x['year']] = x['value']
    countries_2019 = {c: v for c, v in by_country.items() if 2019 in v and 2020 in v}
    top10 = sorted(countries_2019, key=lambda c: countries_2019[c][2019], reverse=True)[:10]
    print("Top 10 by 2019 arrivals:")
    for c in top10:
        v = countries_2019[c]
        drop = (v[2020] - v[2019]) / v[2019] * 100
        print(f"  {c}: 2019={v[2019]/1e6:.1f}M, 2020={v[2020]/1e6:.1f}M ({drop:+.0f}%)")
    return by_country, countries_2019, top10


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — time series showing how arrivals evolved
        - **Country selection**: Top 10 by 2019 arrivals that also have 2020 data (COVID collapse)
        - **Time range**: 2000–2020 to capture the long growth phase and the COVID collapse
        - **Highlights**: Hong Kong lost 94%, Japan 87%; France and China dominated pre-COVID
        """
    )
    return


@app.cell
def _(json, countries_2019, top10):
    all_years = list(range(2000, 2021))
    chart_data = []
    for c in top10:
        v = countries_2019[c]
        series = [round(v[y] / 1e6, 2) if y in v else None for y in all_years]
        label = "HK" if c == "Hong Kong SAR, China" else c
        chart_data.append({"n": label, "s": series, "y0": 2000})
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
