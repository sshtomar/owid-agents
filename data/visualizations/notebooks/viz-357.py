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

        This notebook documents the data pipeline behind viz-357, a trend lines chart
        showing visitor arrivals to top tourist destinations from 1995 to 2020, with
        the COVID-19 collapse as the focal story.
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
    COUNTRIES = [
        "France", "China", "Italy", "Croatia", "Hong Kong SAR, China",
        "Germany", "Greece", "Austria", "Hungary"
    ]
    by_country = {}
    for row in data:
        c = row["countryName"]
        if c in COUNTRIES and row["value"] is not None:
            by_country.setdefault(c, {})[row["year"]] = row["value"]

    print("Countries available:", list(by_country.keys()))
    for c in COUNTRIES:
        if c in by_country:
            vs = by_country[c]
            print(f"  {c}: years {min(vs)}-{max(vs)}, 2019={vs.get(2019,0)/1e6:.0f}M, 2020={vs.get(2020,0)/1e6:.0f}M")
    return COUNTRIES, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- multi-series time-series with hover isolation
        - **Country selection**: Top 9 destinations with available 2020 data; France, China, Italy are the top 3
        - **Time range**: 1995-2020; 2020 captures the COVID collapse
        - **Highlights**: France peaked at 218M; China fell 81% in 2020; Hong Kong near-zero (-94%)
        - **Values in millions** of arrivals for readability
        """
    )
    return


@app.cell
def _(json, COUNTRIES, by_country):
    chart_data = []
    for c in COUNTRIES:
        if c not in by_country:
            continue
        vs = by_country[c]
        y0 = min(vs.keys())
        full_years = list(range(y0, 2021))
        series = [round(vs[y] / 1e6, 2) if y in vs else None for y in full_years]
        label = "Hong Kong" if "Hong Kong" in c else c
        chart_data.append({"n": label, "s": series, "y0": y0})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
