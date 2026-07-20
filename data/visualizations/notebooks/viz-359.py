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
        # Women's Age at First Marriage, 1960–2018 — Methodology

        Trend lines showing the singulate mean age at first marriage for women
        across countries at different development levels.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-SMAM-FE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    targets = {"Hungary","Denmark","Finland","Italy","Germany","Australia","Indonesia","India","Bangladesh","Ghana"}
    by_country = defaultdict(list)
    for row in data:
        if row["countryName"] in targets and row["value"] is not None:
            by_country[row["countryName"]].append({"y": row["year"], "v": round(row["value"], 1)})
    for c in sorted(targets):
        if c in by_country:
            pts = sorted(by_country[c], key=lambda x: x["y"])
            print(f"{c}: {pts[0]['y']}–{pts[-1]['y']}, {pts[0]['v']} → {pts[-1]['v']} yrs")
    return by_country, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows multi-decade trajectory for each country
        - **Country selection**: Mix of Northern Europe (Denmark, Finland, Hungary), Southern Europe/Oceania
          (Italy, Germany, Australia), and South/Southeast Asia and Africa (India, Bangladesh, Indonesia, Ghana)
        - **Story**: European women went from marrying at ~22 to ~32; South Asian women from ~17 to ~21.
          The gap is persistent. All countries show an upward trend — a global social transformation.
        - **Highlights**: Denmark rose fastest among Nordics (+9.8 yrs); Bangladesh remains the lowest
          but also rose (+2.4 yrs since 1974)
        """
    )
    return


@app.cell
def _(json, by_country):
    order = ["Hungary","Denmark","Finland","Italy","Germany","Australia","Indonesia","India","Bangladesh","Ghana"]
    chart_data = [
        {"n": c, "pts": sorted(by_country[c], key=lambda x: x["y"])}
        for c in order if c in by_country
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
