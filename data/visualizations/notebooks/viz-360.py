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
        # Natural Resources Rents as Share of GDP -- Methodology

        Trend lines for resource-dependent countries showing total rents from oil,
        gas, coal, minerals, and forests as % of GDP, 2000-2021. Rents spike with
        commodity booms and crash with busts — illustrating the "resource curse" risk.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-TOTL-RT-ZS.json"
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
            by_country[c] = []
        by_country[c].append((p["year"], p["value"]))

    country_map = {
        'Iraq': 'Iraq', 'Congo, Rep.': 'Congo Rep.', 'Angola': 'Angola',
        'Iran, Islamic Rep.': 'Iran', 'Azerbaijan': 'Azerbaijan',
        'Kazakhstan': 'Kazakhstan', 'Guyana': 'Guyana',
        'Congo, Dem. Rep.': 'DR Congo', 'Algeria': 'Algeria', 'Chad': 'Chad'
    }

    chart_data = []
    for orig, display in country_map.items():
        if orig in by_country:
            pts = sorted(by_country[orig])
            pts2000 = [(y, round(v, 1)) for y, v in pts if y >= 2000]
            sampled = [(y, v) for y, v in pts2000 if y % 2 == 0 or y == pts2000[-1][0]]
            chart_data.append({"n": display, "pts": [{"y": y, "v": v} for y, v in sampled]})
            print(f"  {display}: {pts2000[0][1]:.1f}% (2000) -> {pts2000[-1][1]:.1f}% ({pts2000[-1][0]})")
    return chart_data, by_country, country_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with hover isolation and annotation band
        - **Color**: 10 distinct editorial colors
        - **Story**: Iraq peaked near 65% of GDP during the 2004-2008 oil boom.
          Guyana's rents jumped to 34% in 2021 from near zero — driven by new
          offshore oil discovery. The 2014-2016 price collapse is visible across all.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
