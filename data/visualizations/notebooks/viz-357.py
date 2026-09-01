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
        # Intentional Homicide Rates — Methodology

        Visualizes divergent trends in homicide rates across 11 countries from 1990 to 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = ['Jamaica', 'Ecuador', 'Colombia', 'Honduras', 'Brazil',
               'Estonia', 'Croatia', 'Italy', 'Germany', 'France', 'Japan']
    filtered = [r for r in data if r["value"] is not None and r["countryName"] in targets]
    print(f"After filtering to {len(targets)} countries: {len(filtered)} rows")
    return filtered, targets


@app.cell
def _(filtered, targets):
    from collections import defaultdict
    by_country = defaultdict(list)
    for r in filtered:
        by_country[r["countryName"]].append({"y": r["year"], "v": round(r["value"], 2)})
    chart_data = [
        {"n": c, "pts": sorted(by_country[c], key=lambda x: x["y"])}
        for c in targets if c in by_country
    ]
    for item in chart_data:
        first, last = item["pts"][0], item["pts"][-1]
        change = (last["v"] - first["v"]) / first["v"] * 100
        print(f"  {item['n']}: {first['v']} ({first['y']}) -> {last['v']} ({last['y']}) ({change:+.0f}%)")
    return by_country, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows full 33-year trajectory and enables comparison of trajectories
        - **Country selection**: Balanced mix of rising (Ecuador, Jamaica, Honduras), stable (Brazil), and declining (Colombia, Estonia, Croatia, Italy, France, Germany, Japan)
        - **Color encoding**: Warm colors (red/orange) for rising rates; cool greens for declining
        - **Key story**: Ecuador surged 437% from 1990 to 2023; Colombia fell 67% from its peak of 86 per 100k
        - **Label collision**: resolveCollisions() applied to right-side endpoint labels with 12px min gap
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
