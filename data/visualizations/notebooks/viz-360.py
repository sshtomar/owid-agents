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
        # Fossil Fuel Electricity Transition -- Methodology

        Slope chart comparing fossil fuel electricity share in 2000 vs 2023,
        showing which countries have transitioned away from coal, oil, and gas.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-FOSL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    selected = [
        "Denmark", "Kenya", "Finland", "Czechia", "Hungary", "Greece",
        "Ireland", "Italy", "Australia", "Germany",
        "China", "India", "Indonesia", "Algeria", "Bangladesh",
        "Brazil", "France"
    ]

    chart_data = []
    for c in selected:
        if c in by_country:
            vals = by_country[c]
            yr_b = max(y for y in vals.keys() if y >= 2020)
            if 2000 in vals:
                chart_data.append({
                    "n": c,
                    "a": round(vals[2000], 1),
                    "b": round(vals[yr_b], 1)
                })

    print(f"Countries: {len(chart_data)}")
    for item in chart_data:
        drop = item["a"] - item["b"]
        print(f"  {item['n']}: {item['a']}% -> {item['b']}% (drop {drop:.1f}pp)")
    return chart_data, by_country, selected


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
