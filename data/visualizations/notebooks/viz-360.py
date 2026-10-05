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
        # DPT Immunization Coverage (1980–2024) -- Methodology

        Documents the data pipeline behind viz-360.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IDPT.json"
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
    print(f"Value range: {min(values):.0f}% - {max(values):.0f}%")
    return countries, filtered, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid -- many countries in a compact overview
        - **Country selection**: 20 countries showing diverse vaccination trajectories
        - **Sorting**: By 2024 value ascending (lowest first), so progress is visible
        - **Story**: Almost all countries improved dramatically. Even Chad rose from 3% to 68%.
        """
    )
    return


@app.cell
def _(json, filtered):
    target = [
        "Chad", "Ethiopia", "Kenya", "Ghana", "Angola", "Congo, Dem. Rep.",
        "Haiti", "Bolivia", "India", "Bangladesh", "Cambodia", "Indonesia",
        "Afghanistan", "China", "Brazil", "France", "Germany", "Japan",
        "Greece", "Croatia"
    ]
    chart_data = []
    for name in target:
        pts = sorted([d for d in filtered if d["countryName"] == name], key=lambda x: x["year"])
        if not pts:
            continue
        sampled = [p for p in pts if (p["year"] - 1980) % 4 == 0 or p["year"] == 2024]
        sampled = sorted(sampled, key=lambda x: x["year"])
        if not sampled:
            continue
        vals = [round(p["value"], 0) for p in sampled]
        chart_data.append({"n": name, "s": vals, "y0": sampled[0]["year"], "e": vals[0], "l": vals[-1]})
    chart_data.sort(key=lambda x: x["l"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
