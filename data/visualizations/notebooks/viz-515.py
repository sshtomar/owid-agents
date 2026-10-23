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
        # EU Crime Perception (sdg_16_20) -- Methodology

        Slope chart showing the percentage of EU/EEA residents who feel unsafe walking alone at night,
        comparing 2010 vs 2020. Data from Eurostat's sustainable development goal indicator sdg_16_20.
        Only the 'total' subgroup (not poverty strata) is used.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "eu--sdg_16_20.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for r in data:
        c = r["countryName"]
        y = r["year"]
        if r["value"] is not None and y not in by_country[c]:
            by_country[c][y] = r["value"]

    chart_data = []
    for c, vals in by_country.items():
        a = vals.get(2010)
        b = vals.get(2020)
        if a is not None and b is not None:
            chart_data.append({"n": c, "a": round(a, 1), "b": round(b, 1)})

    chart_data.sort(key=lambda x: x["a"], reverse=True)
    print(f"Countries with both 2010 + 2020: {len(chart_data)}")
    for cd in chart_data:
        delta = round(cd["b"] - cd["a"], 1)
        direction = "UP" if delta > 0 else "down"
        print(f"  {cd['n']}: {cd['a']} -> {cd['b']} ({delta:+.1f}) [{direction}]")
    print()
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
