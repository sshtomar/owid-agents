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
        # Forest Rents (% of GDP) -- Methodology

        Documents the data pipeline for the forest rents visualization.
        Forest rents capture the economic value extracted from timber and
        other forest products as a share of GDP.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-FRST-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and d["year"] >= 1980 and d["year"] <= 2021]
    countries = ["Congo, Dem. Rep.", "Burundi", "Central African Republic",
                 "Guinea-Bissau", "Ethiopia", "Ghana", "Guyana", "Cameroon"]
    by_country = {}
    for row in filtered:
        if row["countryName"] in countries:
            by_country.setdefault(row["countryName"], []).append(row)
    for c, pts in by_country.items():
        pts_sorted = sorted(pts, key=lambda x: x["year"])
        vals = [p["value"] for p in pts_sorted]
        print(f"{c}: {pts_sorted[0]['year']}-{pts_sorted[-1]['year']}, max={max(vals):.1f}%, latest={vals[-1]:.1f}%")
    return by_country, countries, filtered


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows forest-dependent economies and how their
          dependence has changed over 40 years
        - **Country selection**: Focused on Central and West Africa (Congo DRC, CAR, Burundi,
          Guinea-Bissau) where forest rents are highest; plus Ghana and Ethiopia showing
          decline from once-high levels, Guyana for South American contrast, Cameroon for mid-level
        - **Time range**: 1980-2021, captures the colonial timber era through present
        - **Story**: Congo DRC is still extracting 9% of GDP from forests.
          Burundi peaked at 40% but now 14%. Ethiopia fell from 36% to 6%.
          All of these are among the world's poorest nations — forest dependence often reflects
          lack of economic alternatives, not sustainable forestry.
        - **Label shortening**: "Central African Republic" -> "C. Afr. Rep.", "Guinea-Bissau" -> unchanged,
          "Congo, Dem. Rep." -> "Congo DRC"
        """
    )
    return


@app.cell
def _(json, by_country):
    label_map = {
        "Congo, Dem. Rep.": "Congo DRC",
        "Central African Republic": "C. Afr. Rep.",
    }
    chart_data = []
    order = ["Congo, Dem. Rep.", "Burundi", "Central African Republic", "Guinea-Bissau", "Ethiopia", "Ghana", "Guyana", "Cameroon"]
    for c in order:
        pts = sorted(by_country.get(c, []), key=lambda x: x["year"])
        if pts:
            chart_data.append({
                "n": label_map.get(c, c),
                "s": [round(p["value"], 2) for p in pts],
                "y0": pts[0]["year"]
            })
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
