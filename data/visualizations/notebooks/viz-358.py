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
        # Old-Age Dependency Ratio Trend Lines — Methodology

        Trend lines for 12 countries showing elderly (65+) as a share of working-age (15-64)
        population from 1960 to 2024. Sampled every 5 years plus 2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_country = {}
    for p in data:
        if p["value"] is None:
            continue
        c = p["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][p["year"]] = p["value"]

    selected = {
        "Japan": "Japan", "Italy": "Italy", "Germany": "Germany",
        "Korea, Rep.": "South Korea", "France": "France", "China": "China",
        "Brazil": "Brazil", "India": "India", "Argentina": "Argentina",
        "Kenya": "Kenya", "Ethiopia": "Ethiopia", "Bangladesh": "Bangladesh",
    }
    step_years = list(range(1960, 2021, 5)) + [2024]

    output = []
    for wbname, display in selected.items():
        pts = []
        for y in step_years:
            if y in by_country.get(wbname, {}):
                pts.append({"y": y, "v": round(by_country[wbname][y], 1)})
        if pts:
            output.append({"n": display, "pts": pts})

    output.sort(key=lambda x: x["pts"][-1]["v"] if x["pts"] else 0, reverse=True)
    for o in output:
        print(f"{o['n']}: {len(o['pts'])} pts, 2024={o['pts'][-1]['v']}")
    return (output,)


@app.cell
def _(json, output):
    print(json.dumps(output, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
