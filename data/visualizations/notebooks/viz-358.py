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
        # Age Dependency Ratio — Methodology

        Documents the data pipeline behind viz-358.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x['value'] is not None:
            by_country[x['countryName']][x['year']] = x['value']
    countries = ['Japan', 'Korea, Rep.', 'China', 'India', 'Nigeria', 'United States',
                 'Germany', 'Brazil', 'Ethiopia', 'Mexico', 'Egypt, Arab Rep.']
    for c in countries:
        v = by_country.get(c, {})
        if v:
            print(f"{c}: 1960={v.get(1960, 'N/A'):.1f}, 2024={v.get(2024, v.get(2023, 'N/A')):.1f}")
    return by_country, countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — tracks the dependency ratio over six decades
        - **Country selection**: Diverse economies showing contrasting demographic paths
        - **Time range**: 1960–2024 to show full demographic transition arc
        - **Highlights**: Japan reversed from low to high (aging); South Korea, China, Brazil fell sharply;
          Ethiopia remained high; India still declining
        """
    )
    return


@app.cell
def _(json, by_country):
    name_map = {
        'Japan': 'Japan', 'Korea, Rep.': 'South Korea', 'China': 'China',
        'India': 'India', 'Nigeria': 'Nigeria', 'United States': 'United States',
        'Germany': 'Germany', 'Brazil': 'Brazil', 'Ethiopia': 'Ethiopia',
        'Mexico': 'Mexico', 'Egypt, Arab Rep.': 'Egypt'
    }
    all_years = list(range(1960, 2025))
    chart_data = []
    for orig, label in name_map.items():
        v = by_country.get(orig, {})
        if v:
            series = [round(v[y], 1) if y in v else None for y in all_years]
            chart_data.append({"n": label, "s": series, "y0": 1960})
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
