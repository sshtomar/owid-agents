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
        # ATMs per 100,000 Adults — Methodology

        Visualizes the rise and (in high-income countries) the subsequent decline
        of ATM infrastructure as digital payment methods displace cash machines.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FB-ATM-TOTL-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = ["Korea, Rep.", "Japan", "France", "Germany", "Brazil", "China", "India"]
    filtered = [d for d in data if d["countryName"] in targets and d["value"] is not None]
    print(f"Filtered to {len(filtered)} rows for {len(targets)} countries")
    return filtered, targets


@app.cell
def _(filtered):
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in filtered:
        by_country[row["countryName"]].append((row["year"], row["value"]))
    for c, vals in sorted(by_country.items()):
        peak_year = max(vals, key=lambda x: x[1])
        latest = max(vals, key=lambda x: x[0])
        print(f"{c}: peak {peak_year[1]:.0f} ({peak_year[0]}), latest {latest[1]:.0f} ({latest[0]})")
    return by_country,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the arc of ATM density over time
        - **Country selection**: 3 high-income (peaked & declining), 2 mid-income (plateauing), 2 emerging (still growing)
        - **Time range**: 2004–2024 (full series availability)
        - **Highlights**: Korea peaks at 289, Japan/France/Germany now declining; China had explosive growth 2006–2018; India still at 25
        """
    )
    return


@app.cell
def _(json, filtered):
    from collections import defaultdict
    targets = ["Korea, Rep.", "Japan", "France", "Germany", "Brazil", "China", "India"]
    by_country = defaultdict(dict)
    for row in filtered:
        by_country[row["countryName"]][row["year"]] = row["value"]

    series = []
    for name in targets:
        vals = by_country.get(name, {})
        pts = [{"y": yr, "v": round(vals[yr], 1)} for yr in sorted(vals) if 2004 <= yr <= 2024]
        if len(pts) >= 10:
            series.append({"n": name, "pts": pts})

    print(json.dumps(series, separators=(",", ":")))
    return series,


if __name__ == "__main__":
    app.run()
