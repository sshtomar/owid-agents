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
        # Youth Population Share (1990 vs 2024) -- Methodology

        Documents the data pipeline behind viz-358.
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
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    values = [d["value"] for d in filtered]
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f}% - {max(values):.1f}%")
    return countries, filtered, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- comparing two time points (1990, 2024) across 22 countries
        - **Country selection**: Curated to show full spectrum from Chad/DRC (still >45%) to South Korea (10.6%)
        - **Time points**: 1990 (before major demographic transitions) and 2024 (latest)
        - **Color**: By magnitude of decline -- countries that dropped the most get coolest color
        - **Story**: South Korea dropped 15pp in 34 years; sub-Saharan Africa barely moved
        """
    )
    return


@app.cell
def _(json, filtered):
    target = [
        "Japan", "Korea, Rep.", "Germany", "France", "Greece", "Croatia", "Italy",
        "China", "Brazil", "India", "Bangladesh", "Indonesia", "Cambodia",
        "Ethiopia", "Kenya", "Ghana", "Chad", "Angola", "Congo, Dem. Rep.",
        "Afghanistan", "Haiti", "Bolivia"
    ]
    chart_data = []
    for name in target:
        pts_1990 = [d for d in filtered if d["countryName"] == name and d["year"] == 1990]
        pts_2024 = [d for d in filtered if d["countryName"] == name and d["year"] == 2024]
        if pts_1990 and pts_2024:
            chart_data.append({
                "n": name,
                "a": round(pts_1990[0]["value"], 1),
                "b": round(pts_2024[0]["value"], 1)
            })
    chart_data.sort(key=lambda x: -x["b"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
