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
        # Consumer Price Inflation — Methodology

        Trend lines showing annual consumer price inflation (%) for 7 major economies from 2000 to 2024. Highlights the 2021-2022 global inflation surge.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FP-CPI-TOTL-ZG.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ["Germany", "India", "Japan", "Brazil", "Chile", "Australia", "Korea, Rep."]
    by_country = {}
    for row in data:
        c = row["countryName"]
        if c in selected and row["value"] is not None:
            by_country.setdefault(c, {})[row["year"]] = row["value"]

    for c in selected:
        if c in by_country:
            print(f"  {c}: 2022={by_country[c].get(2022, 'n/a'):.1f}%")
    return by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows synchronised 2022 spike across diverse economies
        - **Country selection**: Mix of advanced (Germany, Japan, South Korea, Australia) and emerging (India, Brazil, Chile)
        - **Time range**: 2000–2024 covers two commodity shocks (2008, 2022) and the COVID deflation dip
        - **Highlights**: Japan broke out of decade-long deflation in 2022; Chile hit 11.6% in 2022
        """
    )
    return


@app.cell
def _(json, by_country, selected):
    labels = {"Korea, Rep.": "South Korea"}
    chart_data = []
    for c in selected:
        if c in by_country:
            pts = [{"y": y, "v": round(by_country[c][y], 2)} for y in range(2000, 2025) if y in by_country[c]]
            chart_data.append({"n": labels.get(c, c), "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
