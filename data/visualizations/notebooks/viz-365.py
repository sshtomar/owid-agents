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
        # Gross Savings Rate -- Methodology

        Trend lines showing gross savings (% of GNI) for key economies, 1990-2021.
        Story: East Asian economies save significantly more than Western nations.
        Source: World Bank NY.GNS.ICTR.GN.ZS
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GNS-ICTR-GN-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    countries = ["China", "Korea, Rep.", "India", "Japan", "Germany", "France", "Brazil"]
    years = list(range(1990, 2022, 3))
    chart_data = []
    for cn in countries:
        pts = sorted(
            [(p["year"], round(p["value"], 1)) for p in data if p["countryName"] == cn and p["year"] in years and p["value"] is not None],
            key=lambda x: x[0]
        )
        if pts:
            series = [v for _, v in pts]
            chart_data.append({"n": cn, "s": series, "y0": pts[0][0], "step": 3})
            print(f"{cn}: {series}")
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, countries, pts, series, years


if __name__ == "__main__":
    app.run()
