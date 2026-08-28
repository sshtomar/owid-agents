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

        Documents the trend lines visualization showing aging trajectories
        for 8 countries from 1990 to 2023.
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
    import re
    country_data = {}
    for pt in data:
        code = pt["country"]
        if re.match(r"^[A-Z]{2}$", code) and pt["value"] is not None:
            cn = pt["countryName"]
            yr = pt["year"]
            if cn not in country_data:
                country_data[cn] = {}
            country_data[cn][yr] = pt["value"]
    focus = ["Japan", "Korea, Rep.", "Italy", "Germany", "France", "China", "Brazil", "India"]
    years = [1990, 1995, 2000, 2005, 2010, 2015, 2020, 2023]
    for cn in focus:
        if cn in country_data:
            vals = [country_data[cn].get(y) for y in years]
            print(f"{cn}: {[round(v, 1) if v else None for v in vals]}")
    return cn, code, country_data, focus, pt, re, vals, years, yr


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 8 data points per country over 33 years; evolution over time is the story
        - **Country selection**: Japan (world leader), Korea (fastest-aging), Western Europe (established), China/Brazil/India (emerging)
        - **Color**: Each country distinct; warm tones for highest-dependency countries
        - **Story**: Japan's dependency ratio tripled since 1990; Korea is now the fastest-aging country in history
        """
    )
    return


@app.cell
def _(cn, country_data, focus, json, years):
    chart_data = []
    for name in focus:
        if name in country_data:
            pts = [{"y": yr, "v": round(country_data[name][yr], 1)} for yr in years if yr in country_data[name]]
            if len(pts) >= 6:
                display = name.replace(", Rep.", "")
                chart_data.append({"n": display, "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, display, name, pts


if __name__ == "__main__":
    app.run()
