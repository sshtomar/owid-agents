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
        # Current Account Balance Trends -- Methodology

        Shows how major economies have diverged into persistent surplus and deficit
        positions from 2000 to 2024, revealing structural imbalances in global trade.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--BN-CAB-XOKA-GD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for x in data:
        if x["value"] is not None:
            by_country[x["countryName"]][x["year"]] = round(x["value"], 1)
    countries_with_recent = [c for c, m in by_country.items() if any(y >= 2022 for y in m)]
    print(f"Countries with 2022+ data: {len(countries_with_recent)}")
    return (by_country,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows structural divergence over time
        - **Country selection**: 8 economies representing persistent surplus (Germany, Denmark,
          Japan, South Korea, China) and deficit (Canada, Brazil, India) positions
        - **Time range**: 2000-2024 -- captures the full post-dotcom to present era
        - **Story**: Germany transformed from deficit to Europe's largest surplus. Denmark
          reaches 11.5%. China's surplus peaked at 10% in 2007 then narrowed. Canada
          flipped from surplus to deficit after 2008.
        """
    )
    return


@app.cell
def _(json, by_country):
    countries = ["Germany", "Denmark", "Japan", "Korea, Rep.", "China",
                 "Canada", "Brazil", "India"]
    labels = {"Korea, Rep.": "South Korea"}
    chart_data = []
    for c in countries:
        if c not in by_country:
            continue
        ymap = by_country[c]
        series = [ymap.get(y) for y in range(2000, 2025)]
        label = labels.get(c, c)
        chart_data.append({"n": label, "s": series, "y0": 2000})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
