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
        # Renewable Share of Electricity Generation -- Methodology

        Slope chart comparing each country's renewable electricity share in 2000 vs 2024.
        Shows the global clean energy transition over 24 years.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "ember--SHARE-RENEWABLES.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    # Countries to include (major economies + notable cases)
    target = [
        "United States of America", "China", "Germany", "United Kingdom",
        "Denmark", "France", "India", "Brazil", "Japan", "Spain",
        "Portugal", "Lithuania", "Norway", "Kenya", "South Africa",
        "Australia", "Italy", "Netherlands", "Poland", "Sweden"
    ]

    by_name = {}
    for r in data:
        c = r["countryName"]
        if c in target and r["value"] is not None:
            by_name.setdefault(c, {})[r["year"]] = r["value"]

    # Build slope data: only countries with both 2000 and 2024
    slope_data = []
    for c in target:
        vals = by_name.get(c, {})
        if 2000 in vals and 2024 in vals:
            label = "United States" if c == "United States of America" else c
            slope_data.append({"n": label, "a": round(vals[2000], 1), "b": round(vals[2024], 1)})

    print(f"Countries in slope chart: {len(slope_data)}")
    for d in sorted(slope_data, key=lambda x: x["b"] - x["a"], reverse=True):
        print(f"  {d['n']}: {d['a']} -> {d['b']} (+{d['b']-d['a']:.1f})")
    return slope_data, by_name, target


@app.cell
def _(slope_data, json):
    # Export for HTML
    print(json.dumps(slope_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
