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
        # Crude Death Rate by World Region — Methodology

        Trend lines for 6 world regions from 1960 to 2024, sampled every 5 years.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-CDRT-IN.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    REGIONS = [
        "Sub-Saharan Africa",
        "South Asia",
        "East Asia & Pacific",
        "Europe & Central Asia",
        "Latin America & Caribbean",
        "North America",
    ]
    years_step = list(range(1960, 2025, 5))

    by_region = {}
    for p in data:
        cn = p["countryName"]
        if cn not in REGIONS:
            continue
        if p["value"] is None:
            continue
        if cn not in by_region:
            by_region[cn] = {}
        by_region[cn][p["year"]] = round(p["value"], 2)

    print(f"Regions found: {list(by_region.keys())}")
    print(f"Year range: {years_step[0]}-{years_step[-1]}")
    return REGIONS, by_region, years_step


@app.cell
def _(REGIONS, by_region, years_step):
    chart_data = []
    for region in REGIONS:
        if region not in by_region:
            continue
        s = [by_region[region].get(y) for y in years_step]
        chart_data.append({"n": region, "s": s, "y0": years_step[0], "step": 5})
        vals = [v for v in s if v is not None]
        print(f"{region}: {s[0]:.1f} -> {vals[-1]:.1f}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows 64-year trajectory for 6 major regions
        - **Region selection**: All 6 standard World Bank regions with consistent data
        - **Sampling**: Every 5 years for clarity; detailed year data available in dataset
        - **Highlights**: Sub-Saharan Africa's dramatic decline, Europe's aging-driven plateau
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
