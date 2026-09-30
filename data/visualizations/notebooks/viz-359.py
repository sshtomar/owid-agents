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
        # The Aging Divide -- Methodology

        Old-age dependency ratio (elderly per 100 working-age people), 1960-2024.
        Source: World Bank SP.POP.DPND.OL.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = {}
    for pt in data:
        c = pt["countryName"]
        if c not in countries:
            countries[c] = {}
        if pt["value"] is not None:
            countries[c][pt["year"]] = round(pt["value"], 2)

    selected = ["Japan", "Italy", "Germany", "France", "Korea, Rep.", "China", "Brazil", "India"]
    labels = {"Korea, Rep.": "Korea"}
    years = list(range(1960, 2025))
    chart_data = []
    for c in selected:
        if c in countries:
            series = [countries[c].get(y) for y in years]
            chart_data.append({"n": labels.get(c, c), "s": series})
    print(f"Chart data: {len(chart_data)} countries, {len(years)} years (1960-2024)")
    print(f"Japan 2024: {countries['Japan'].get(2024)}")
    print(f"India 2024: {countries['India'].get(2024)}")
    return chart_data, countries, labels, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- diverging trajectories tell the story
        - **Countries**: 8 countries spanning extreme cases (Japan leading, India minimal)
        - **Y axis**: Elderly per 100 working-age people
        - **Key insight**: Japan at 50.7 (1 elderly per 2 workers); India still near 10
        - **Story**: East Asia (Japan, Korea, China) aging rapidly; South Asia aging slowly
        """
    )
    return


if __name__ == "__main__":
    app.run()
