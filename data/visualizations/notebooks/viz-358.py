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
        # Child Wasting -- Methodology

        Shows the 15 countries with the highest rates of acute malnutrition
        (wasting) in children under 5, based on most recent available data.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-WAST-ZS.json"
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

    skip_words = ["income", "dividend", "OECD", "World", "Asia", "Africa",
                  "Europe", "America", "Arab", "Caribbean", "Pacific",
                  "small states", "region", "Central"]

    def is_aggregate(name):
        return any(w.lower() in name.lower() for w in skip_words)

    latest = {}
    for c, vals in by_country.items():
        if is_aggregate(c):
            continue
        ys = sorted(vals.keys())
        recent = [y for y in ys if y >= 2015]
        if recent:
            yr = max(recent)
            latest[c] = (yr, vals[yr])

    top15 = sorted(latest.items(), key=lambda x: x[1][1], reverse=True)[:15]
    chart_data = [{"n": name, "v": round(val, 1), "y": yr} for name, (yr, val) in top15]
    print(f"Countries in chart: {len(chart_data)}")
    for item in chart_data:
        print(f"  {item['n']} ({item['y']}): {item['v']}%")
    return chart_data, by_country, latest, top15


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
