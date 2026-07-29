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

        Trend lines for 8 countries showing the elderly population (65+) as a share of
        working-age population (15–64) from 1960 to 2020 in 5-year steps.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    countries = {}
    for p in data:
        c = p["countryName"]
        if p["value"] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][p["year"]] = p["value"]
    return (countries,)


@app.cell
def _(countries):
    mapping = {
        "Japan": "Japan", "Italy": "Italy", "Germany": "Germany",
        "France": "France", "Korea, Rep.": "South Korea", "China": "China",
        "Brazil": "Brazil", "India": "India"
    }
    chart_data = []
    for orig, display in mapping.items():
        if orig not in countries:
            continue
        vals = countries[orig]
        series = []
        for yr in range(1960, 2021, 5):
            v = vals.get(yr)
            series.append(round(v, 2) if v is not None else None)
        chart_data.append({"n": display, "s": series})

    print("Series (5-year steps 1960-2020, 13 points):")
    for d in chart_data:
        print(f"  {d['n']}: 1960={d['s'][0]}, 2000={d['s'][8]}, 2020={d['s'][12]}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the demographic aging trajectory clearly
        - **Step**: 5-year intervals to smooth out short-term fluctuations
        - **Country selection**: Mix of fast-aging (Japan, Korea), stable-aging (Europe),
          and slower-aging (China, Brazil, India) trajectories
        - **Color**: Warm for most-aged (Japan, Italy), cool for least-aged (India, Brazil)
        - **Highlights**: Japan 8.9% in 1960 to 49.1% in 2020; South Korea accelerating sharply
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
