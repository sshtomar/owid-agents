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
        # Age Dependency Ratio -- Methodology

        Slope chart comparing age dependency ratio (1960 vs 2024) for 16 selected
        countries. World Bank indicator SP.POP.DPND.
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
    filtered = [r for r in data if r["value"] is not None and r["year"] in (1960, 2024)]
    print(f"Filtered to {len(filtered)} rows (1960 and 2024 only)")
    return (filtered,)


@app.cell
def _(filtered):
    selected = ['Korea, Rep.', 'China', 'Brazil', 'Iran, Islamic Rep.', 'India',
                'Argentina', 'Bangladesh', 'Canada', 'Italy', 'Germany', 'France',
                'Ghana', 'Kenya', 'Japan', 'Ethiopia', 'Congo, Dem. Rep.']
    by_country = {}
    for r in filtered:
        if r["countryName"] in selected:
            if r["countryName"] not in by_country:
                by_country[r["countryName"]] = {}
            by_country[r["countryName"]][r["year"]] = r["value"]
    pairs = [(name, v[1960], v[2024]) for name, v in by_country.items() if 1960 in v and 2024 in v]
    print(f"Countries with both years: {len(pairs)}")
    for name, a, b in sorted(pairs, key=lambda x: x[2]):
        print(f"  {name}: {a:.1f} -> {b:.1f} ({b-a:+.1f})")
    return (pairs,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- best for comparing two time points
        - **Country selection**: Diverse global sample showing demographic spectrum
        - **Highlights**: Korea's remarkable transition, Japan aging, Congo DRC still very high
        - **Color**: Green = large fall (faster demographic transition), red = still high/rising
        """
    )
    return


@app.cell
def _(json, pairs):
    chart_data = [
        {"n": name.replace(", Islamic Rep.", "").replace(", Arab Rep.", "").replace(", Dem. Rep.", " DRC").replace(", Rep.", ""),
         "a": round(a, 1), "b": round(b, 1)}
        for name, a, b in sorted(pairs, key=lambda x: x[2])
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
