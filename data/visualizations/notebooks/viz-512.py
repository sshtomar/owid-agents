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
        # Services Value Added (% of GDP) — Methodology

        Trend lines for 10 economies showing the structural shift toward services, 1980–2024.
        Source dataset: wb--NV-SRV-TOTL-ZS
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-SRV-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = ["China", "India", "Brazil", "France", "Korea, Rep.", "Bangladesh", "Chile", "Australia", "Indonesia", "Argentina"]
    result = []
    for name in target:
        yv = {p["year"]: round(p["value"], 1) for p in data if p["countryName"] == name and p["value"] is not None and p["year"] >= 1980}
        if yv:
            years = sorted(yv.keys())
            pts = [{"y": y, "v": yv[y]} for y in years]
            result.append({"n": name, "pts": pts})
            print(f"{name}: {min(years)}-{max(years)}, v1980={yv.get(1980,'N/A')}, v2024={yv[max(years)]:.1f}%")
    return result, target, yv


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Multi-series trend lines — shows long-run structural transformation
        - **Country selection**: Mix of high-income (France, Australia), emerging (China, Korea, India), and developing (Bangladesh, Indonesia)
        - **Year range**: 1980–2024 (45 years, capturing post-industrialization transitions)
        - **Highlights**: China rose from 22% to 57%; France already at 58% in 1980 and now 71%
        - **Note**: Brazil shows sharp spikes in 1990–1993 due to hyperinflation distorting GDP ratios
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
