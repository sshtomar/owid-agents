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
        # Coal Rents as % of GDP — Methodology

        Trend lines showing the economic dependence of major coal economies on coal
        extraction rents, 1990–2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-COAL-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = ["China", "India", "Indonesia", "Australia", "Kazakhstan", "Colombia",
               "Bosnia and Herzegovina", "Botswana", "Czechia"]
    filtered = [d for d in data if d["countryName"] in targets and d["value"] is not None and d["year"] >= 1990]
    print(f"Filtered to {len(filtered)} rows")
    from collections import defaultdict
    by_country = defaultdict(list)
    for row in filtered:
        by_country[row["countryName"]].append((row["year"], row["value"]))
    for c in targets:
        vals = sorted(by_country.get(c, []))
        if vals:
            peak = max(vals, key=lambda x: x[1])
            print(f"{c}: peak {peak[1]:.2f}% in {peak[0]}")
    return by_country, filtered, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows temporal evolution of coal rents
        - **Country selection**: Top 8 coal-dependent economies by average rents 1990–2021
          (excluded Cabo Verde due to likely data anomaly)
        - **Time range**: 1990–2021 (full series)
        - **Highlights**: Kazakhstan peaked at 4.8% in 2008; China's coal rents spiked 5% in 2008;
          Indonesia has surged since 2020; Czech Republic's coal sector is declining
        - **Annotation**: 2008 commodity price boom marked as reference line
        """
    )
    return


@app.cell
def _(json, by_country, targets):
    series = []
    for name in targets:
        vals = dict(sorted(by_country.get(name, [])))
        pts = [{"y": yr, "v": round(vals[yr], 3)} for yr in sorted(vals)]
        if len(pts) >= 15:
            series.append({"n": name, "pts": pts})
    print(json.dumps(series, separators=(",", ":")))
    return series,


if __name__ == "__main__":
    app.run()
