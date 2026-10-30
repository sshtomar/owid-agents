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
        # Trade in Services (% of GDP) — Methodology

        Documents the data pipeline behind viz-511: trend lines for 8 countries
        showing the divergence between services-specialised economies and
        manufacturing-dominant ones, 1990–2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--BG-GSR-NFSV-GD-ZS.json"
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
        if row.get("value") is not None and row.get("countryName"):
            by_country[row["countryName"]][row["year"]] = row["value"]

    countries = ["Cyprus", "Denmark", "Bahrain", "Estonia", "India", "Germany", "Brazil", "China"]
    filtered = {c: by_country[c] for c in countries}
    print(f"Countries selected: {countries}")
    for c, yrs in filtered.items():
        recent = max(yrs)
        print(f"  {c}: {len(yrs)} years, latest={recent}, value={round(yrs[recent],1)}%")
    return by_country, countries, filtered


@app.cell
def _(filtered, json):
    labels = {"Korea, Rep.": "S. Korea"}
    result = []
    for name, years in filtered.items():
        pts = sorted([{"y": y, "v": round(v, 1)} for y, v in years.items() if 1990 <= y <= 2024], key=lambda x: x["y"])
        label = labels.get(name, name)
        result.append({"n": label, "pts": pts})
    print(json.dumps(result, separators=(",", ":")))
    return (result,)


if __name__ == "__main__":
    app.run()
