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
        # Oil Rents (% of GDP) -- Methodology

        This notebook documents the data pipeline and editorial decisions
        behind the visualization of oil rents as a share of GDP for selected
        petrostate economies.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-PETR-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1970 and d["year"] <= 2021]
    print(f"After filtering: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    countries = [
        "Iraq", "Bahrain", "Angola", "Brunei Darussalam", "Gabon",
        "Iran, Islamic Rep.", "Algeria", "Ecuador", "Azerbaijan", "Guyana", "Kazakhstan"
    ]
    by_country = {}
    for row in filtered:
        c = row["countryName"]
        if c in countries:
            by_country.setdefault(c, []).append(row)
    for c, pts in by_country.items():
        vals = [p["value"] for p in pts]
        print(f"{c}: {len(pts)} pts, max={max(vals):.1f}%")
    return by_country, countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows how oil dependency evolved over decades
        - **Country selection**: Mix of major OPEC-adjacent states and petrostates that report
          data to World Bank. Saudi Arabia, Kuwait, UAE, Russia, Norway, and Nigeria lack
          data in this series; Iraq, Angola, Iran, Algeria, Bahrain, and Brunei fill the story.
        - **Time range**: 1970-2021, capturing oil shocks of 1973, 1979, 1990, 2008, 2014
        - **Highlights**: Iraq and Angola remain highly dependent; Bahrain and Brunei diversified
          significantly; Guyana's emergence as a new petrostate starting 2020
        - **Label names**: Shorten "Iran, Islamic Rep." to "Iran", "Brunei Darussalam" to "Brunei"
        """
    )
    return


@app.cell
def _(json, by_country):
    label_map = {
        "Iran, Islamic Rep.": "Iran",
        "Brunei Darussalam": "Brunei",
    }
    chart_data = []
    for c, pts in sorted(by_country.items()):
        pts_sorted = sorted(pts, key=lambda x: x["year"])
        chart_data.append({
            "n": label_map.get(c, c),
            "s": [round(p["value"], 2) for p in pts_sorted],
            "y0": pts_sorted[0]["year"]
        })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
