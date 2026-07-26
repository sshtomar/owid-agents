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
        # Aquaculture Production -- Methodology

        Trend lines for China, Indonesia, India, Bangladesh, Korea, Chile,
        Japan showing farmed seafood production (million metric tons) 1980-2024.
        China accounts for over 70% of global production.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-FSH-AQUA-MT.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    focus = ["China","Indonesia","India","Bangladesh","Korea, Rep.","Chile","Japan"]
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in data:
        if row["countryName"] in focus and row["value"] is not None and row["year"] >= 1980:
            by_country[row["countryName"]].append({"y": row["year"], "v": round(row["value"]/1e6, 3)})
    chart_data = [{"n": k, "pts": sorted(by_country[k], key=lambda x: x["y"])} for k in focus]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
