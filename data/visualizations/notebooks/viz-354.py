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
        # The World's Demographic Divide -- Methodology

        Slope chart comparing population ages 0-14 as % of total, 1970 vs 2024,
        for 20 countries spanning the full range from Sub-Saharan Africa to East Asia/Europe.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-0014-TO-ZS.json"
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

        - **Chart type**: Slope chart (1970 vs 2024) — shows demographic transition over 54 years
        - **Country selection**: Top 8 highest (Sub-Saharan Africa) + 8 lowest (East Asia/Europe) + 4 notable mid-transitions
        - **Color**: Encodes direction — orange/red for rising or static youth share (demographic pressure);
          green spectrum for declining (successful transition), deepest green for >25pp decline
        - **Notable transitions**: S. Korea went from 42% to 10.6% (-31pp); Iran from 44.6% to 22.4% (-22pp)
        - **Stagnation story**: Chad actually rose from 42.7% to 46.1% — almost half the population is under 15
        """
    )
    return


@app.cell
def _(json):
    chart_data = [
        {"n": "Chad", "a": 42.7, "b": 46.1},
        {"n": "DR Congo", "a": 43.4, "b": 46.0},
        {"n": "Burundi", "a": 44.9, "b": 44.7},
        {"n": "Angola", "a": 45.9, "b": 44.4},
        {"n": "Afghanistan", "a": 43.9, "b": 42.9},
        {"n": "Burkina Faso", "a": 42.4, "b": 41.8},
        {"n": "Benin", "a": 43.2, "b": 41.6},
        {"n": "Cameroon", "a": 42.0, "b": 41.4},
        {"n": "Bangladesh", "a": 44.4, "b": 28.0},
        {"n": "India", "a": 41.4, "b": 24.6},
        {"n": "Indonesia", "a": 42.6, "b": 24.6},
        {"n": "Iran", "a": 44.6, "b": 22.4},
        {"n": "China", "a": 40.8, "b": 16.0},
        {"n": "Brazil", "a": 42.7, "b": 19.7},
        {"n": "Japan", "a": 23.3, "b": 11.4},
        {"n": "Italy", "a": 24.7, "b": 11.9},
        {"n": "Greece", "a": 24.8, "b": 13.2},
        {"n": "Bosnia", "a": 35.2, "b": 13.0},
        {"n": "S. Korea", "a": 42.1, "b": 10.6},
        {"n": "Hong Kong", "a": 38.4, "b": 10.5},
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
