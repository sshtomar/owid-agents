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
        # International Tourism Arrivals -- Methodology

        Trend lines for France, China, Italy, Germany, Japan showing
        arrivals in millions from 1995 to 2020, including COVID-19 crash.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    focus = ["France","China","Italy","Germany","Japan"]
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in data:
        if row["countryName"] in focus and row["value"] is not None and row["year"] >= 1995:
            by_country[row["countryName"]].append({"y": row["year"], "v": round(row["value"]/1e6, 2)})
    chart_data = [{"n": k, "pts": sorted(v, key=lambda x: x["y"])} for k in focus for v_list in [by_country[k]] if v_list]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
