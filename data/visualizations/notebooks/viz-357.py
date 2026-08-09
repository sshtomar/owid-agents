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
        # International Tourism Arrivals -- Methodology

        Trend lines showing tourist arrivals for the world's top 10 most-visited
        countries (1995-2020). Data from World Bank indicator ST.INT.ARVL.
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
    selected = ['France', 'China', 'Italy', 'Hungary', 'Croatia',
                'Hong Kong SAR, China', 'Germany', 'Greece', 'Austria', 'Japan']
    filtered = [r for r in data if r["value"] is not None and r["countryName"] in selected]
    print(f"Filtered to {len(filtered)} rows for top 10 destinations")
    return (filtered,)


@app.cell
def _(filtered):
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    values = [d["value"] for d in filtered]
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Arrivals range: {min(values)/1e6:.1f}M - {max(values)/1e6:.1f}M")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows how arrivals grew over time for each country
        - **Country selection**: Top 10 by 2019 arrivals (actual countries, not regional aggregates)
        - **Time range**: 1995-2020 (full dataset), highlights COVID crash in 2020
        - **Highlights**: France #1, China's rapid rise, 2020 collapse
        """
    )
    return


@app.cell
def _(json, filtered):
    from collections import defaultdict
    series = defaultdict(dict)
    for r in filtered:
        name = r["countryName"].replace(" SAR, China", "")
        series[name][r["year"]] = r["value"]
    chart_data = [
        {"n": name, "pts": [{"y": y, "v": round(v/1e6, 2)} for y, v in sorted(pts.items())]}
        for name, pts in series.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
