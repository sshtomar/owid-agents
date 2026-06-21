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
        # Progress on Safe Drinking Water -- Methodology

        Slope chart showing population using safely managed drinking water services
        (% of population), 2000 vs 2024. "Safely managed" means on-premises, available
        when needed, free from contamination — a higher bar than basic access.
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
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    years = sorted(set(d["year"] for d in filtered))
    print(f"Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f}% - {max(values):.1f}%")
    return values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2024) — shows 24-year trajectory
        - **Country selection**: Mix of big improvers (India +39pp, Bhutan +37pp) and laggards (Chad, DRC)
          plus high-income reference countries (Germany, France, Japan near 100%)
        - **Color**: Green spectrum by improvement magnitude; amber for minimal gain; red for decline
        - **Key story**: India's dramatic gain (+39pp, 1.4 billion people) vs. Chad/DRC stuck below 13%
        - **Data note**: 2024 is latest available; some countries may use 2022/2023 as endpoint
        """
    )
    return


@app.cell
def _(json):
    chart_data = [
        {"n": "Germany", "a": 99.8, "b": 99.9},
        {"n": "France", "a": 97.4, "b": 99.7},
        {"n": "Japan", "a": 97.9, "b": 98.7},
        {"n": "Kazakhstan", "a": 63.2, "b": 91.5},
        {"n": "Jordan", "a": 55.5, "b": 89.0},
        {"n": "Brazil", "a": 75.8, "b": 88.6},
        {"n": "India", "a": 37.6, "b": 76.4},
        {"n": "Albania", "a": 49.1, "b": 70.8},
        {"n": "Bhutan", "a": 28.4, "b": 65.6},
        {"n": "Honduras", "a": 41.8, "b": 65.5},
        {"n": "Gambia", "a": 23.3, "b": 48.2},
        {"n": "Ghana", "a": 14.4, "b": 42.9},
        {"n": "Afghanistan", "a": 11.5, "b": 30.6},
        {"n": "Indonesia", "a": 23.5, "b": 30.5},
        {"n": "Cambodia", "a": 17.1, "b": 30.0},
        {"n": "Benin", "a": 14.2, "b": 17.7},
        {"n": "Ethiopia", "a": 5.4, "b": 13.5},
        {"n": "DR Congo", "a": 12.2, "b": 11.9},
        {"n": "Chad", "a": 5.5, "b": 6.3},
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
