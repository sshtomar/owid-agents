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
        # Gross Savings (% of GDP) -- Methodology

        Trend lines showing how savings rates evolved 1980-2024 across
        China, India, Germany, Japan, South Korea, Brazil, and Greece.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNS-ICTR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    focus = {"China","India","Germany","Japan","Korea, Rep.","Brazil","Greece"}
    filtered = [d for d in data if d["countryName"] in focus and d["value"] is not None and d["year"] >= 1980]
    print(f"After filtering: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered, json):
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in filtered:
        by_country[row["countryName"]].append({"y": row["year"], "v": round(row["value"], 1)})
    chart_data = [{"n": k, "pts": sorted(v, key=lambda x: x["y"])} for k, v in by_country.items()]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
