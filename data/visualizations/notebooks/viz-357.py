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
        # Population Growth Rate (1961-2024) -- Methodology

        Documents the data pipeline behind viz-357.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
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
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    values = [d["value"] for d in filtered]
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.2f}% - {max(values):.2f}%")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- best for showing long-run trajectory of multiple entities
        - **Country selection**: Mix of regional aggregates (World, Sub-Saharan Africa, South Asia)
          and individual countries across all stages of demographic transition
        - **Time range**: 1961-2024, sampled every 4 years for compactness
        - **Highlights**: Sub-Saharan Africa remains above 2.4%; China turned negative; Japan/Korea
          now below zero; India fell from 2.4% to 0.9%
        """
    )
    return


@app.cell
def _(json, filtered):
    target = [
        "Sub-Saharan Africa", "South Asia", "India", "Brazil", "World",
        "China", "Germany", "Japan", "Korea, Rep.", "France",
        "Ethiopia", "Kenya", "Ghana", "Bangladesh"
    ]
    chart_data = []
    for name in target:
        pts = sorted([d for d in filtered if d["countryName"] == name], key=lambda x: x["year"])
        if not pts:
            continue
        sampled = [p for p in pts if (p["year"] - 1961) % 4 == 0]
        if pts[-1]["year"] not in [p["year"] for p in sampled]:
            sampled.append(pts[-1])
        sampled = sorted(sampled, key=lambda x: x["year"])
        vals = [round(p["value"], 2) for p in sampled]
        chart_data.append({"n": name, "s": vals, "y0": sampled[0]["year"], "step": 4})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
