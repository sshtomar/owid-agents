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
        # Anemia in Women: 2000 vs 2023 -- Methodology

        Slope chart comparing anemia prevalence among non-pregnant women aged 15-49
        in 2000 vs 2023. Selects the 30 highest-burden countries in 2023 to show
        which made progress and which worsened.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-NPRG-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    skip_kw = ('Africa', 'East', 'Europe', 'Latin', 'Middle', 'North', 'South', 'Sub', 'World', 'High', 'Low', 'Lower', 'Upper', 'Least', 'Fragile', 'Small', 'IBRD', 'IDA', 'OECD', 'Arab', 'Central', 'Pacific', 'Caribbean', 'Heavily', 'income', 'dividend', 'region', 'members', 'countries', 'states', 'Eurasia', 'Asia', 'America', 'Euro')
    by_country = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is None or any(k.lower() in c.lower() for k in skip_kw):
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][y] = v
    slope_data = []
    for c, ydata in by_country.items():
        a = ydata.get(2000) or ydata.get(2001)
        b = ydata.get(2023) or ydata.get(2022) or ydata.get(2021)
        if a is not None and b is not None:
            slope_data.append({"n": c, "a": round(a, 1), "b": round(b, 1)})
    slope_data.sort(key=lambda x: x["b"], reverse=True)
    selected = slope_data[:30]
    print(f"Countries with slope data: {len(slope_data)}, selected: {len(selected)}")
    worsened = [(d["n"], d["a"], d["b"]) for d in selected if d["b"] > d["a"]]
    print(f"Countries where anemia worsened: {worsened}")
    return by_country, selected, slope_data, worsened


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- two time points, many entities, clear direction of change
        - **Country selection**: Top 30 highest-burden in 2023 (>31%)
        - **Color**: Red/orange = worsened, amber/green = improved
        - **Surprise findings**: India's anemia rose 4 pp; Afghanistan rose 17 pp; most W. Africa improved
        """
    )
    return


@app.cell
def _(json, selected):
    print(json.dumps(selected, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
