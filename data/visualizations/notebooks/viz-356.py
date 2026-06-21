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
        # Hypertension Treatment Coverage -- Methodology

        Horizontal bar chart showing effective hypertension treatment coverage
        (controlled hypertension among adults 30-79, age-standardized %).
        Most recent year per country, ranging from 2010 to 2019.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_HYP_CONTROL_A.json"
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

        - **Chart type**: Horizontal bar chart — single metric comparison across countries, ranked
        - **Country selection**: 30 countries from WHO data: top performers + key populous countries + lowest
        - **Color**: Green spectrum for high coverage, amber-red for low — diverging to show crisis
        - **Key story**: Global median below 15%; even richest countries top out at ~60%
        - **Data caveat**: Countries have different reference years (2010-2019); not perfectly comparable
        - **Highlights**: Canada 60.7% tops; China 2.6% despite its massive hypertension burden
        """
    )
    return


@app.cell
def _(json):
    chart_data = [
        {"n": "Canada", "v": 60.7},
        {"n": "S. Korea", "v": 53.8},
        {"n": "United States", "v": 50.3},
        {"n": "Costa Rica", "v": 49.7},
        {"n": "Portugal", "v": 38.4},
        {"n": "Venezuela", "v": 38.4},
        {"n": "Honduras", "v": 37.9},
        {"n": "Belgium", "v": 36.3},
        {"n": "Cyprus", "v": 36.2},
        {"n": "Czechia", "v": 35.5},
        {"n": "Singapore", "v": 34.9},
        {"n": "Slovakia", "v": 34.9},
        {"n": "Brazil", "v": 34.6},
        {"n": "Germany", "v": 34.3},
        {"n": "South Africa", "v": 23.6},
        {"n": "Japan", "v": 23.5},
        {"n": "Russia", "v": 20.5},
        {"n": "Nigeria", "v": 10.4},
        {"n": "India", "v": 8.4},
        {"n": "Cameroon", "v": 7.1},
        {"n": "Senegal", "v": 6.0},
        {"n": "Tajikistan", "v": 4.6},
        {"n": "Mozambique", "v": 4.3},
        {"n": "Uganda", "v": 4.0},
        {"n": "Kenya", "v": 3.2},
        {"n": "China", "v": 2.6},
        {"n": "Zambia", "v": 2.3},
        {"n": "Ethiopia", "v": 2.1},
        {"n": "Tanzania", "v": 2.1},
        {"n": "Indonesia", "v": 1.2},
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
