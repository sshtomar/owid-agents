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

        Trend lines for 8 major tourist destinations, 1995-2020.
        The 2020 data point captures the COVID-19 collapse.
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
    picks = {'China', 'Italy', 'Germany', 'Japan', 'Greece', 'Korea, Rep.', 'Australia', 'Indonesia'}
    years = list(range(1995, 2021))

    by_country = {}
    for p in data:
        cn = p["countryName"]
        if cn not in picks:
            continue
        if p["value"] is None:
            continue
        if cn not in by_country:
            by_country[cn] = {}
        by_country[cn][p["year"]] = p["value"]

    print(f"Countries: {list(by_country.keys())}")
    print(f"Year range: {min(years)}-{max(years)}")
    return by_country, picks, years


@app.cell
def _(by_country, years):
    name_map = {"Korea, Rep.": "South Korea"}
    chart_data = []
    for country, vals in by_country.items():
        s = [round(vals.get(y) / 1e6, 2) if vals.get(y) else None for y in years]
        chart_data.append({"n": name_map.get(country, country), "s": s, "y0": years[0]})

    chart_data.sort(key=lambda x: -(max(v for v in x["s"] if v is not None)))
    print(f"Series count: {len(chart_data)}")
    for c in chart_data:
        vals = [v for v in c["s"] if v is not None]
        print(f"  {c['n']}: peak={max(vals):.1f}M, 2020={c['s'][-1]}M")
    return chart_data, name_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows evolution of tourism over 26 years
        - **Country selection**: 8 countries with consistent data; France excluded due to methodology (counts day visitors, inflating totals to 200M+)
        - **Time range**: 1995-2020; ends at 2020 to capture the COVID collapse
        - **Highlights**: China's 3.5x growth, Japan's 10x growth, universal 2020 crash
        - **Color**: Warm-to-cool ramp by peak arrivals rank
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
