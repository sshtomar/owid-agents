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
        # International Tourism Arrivals (1995–2020) -- Methodology

        Documents the data pipeline behind viz-359.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows the 1995-2019 boom and 2020 COVID collapse
        - **Country selection**: Top 8 destinations with 2020 data and >5M arrivals in 2019
        - **Key insight**: Japan/Hong Kong lost 87-94% of arrivals; France/Hungary lost only ~46-48%
        - **Note**: France values include day-trippers from neighboring countries, inflating counts
        """
    )
    return


@app.cell
def _(json, filtered):
    top_countries = ["France", "China", "Italy", "Croatia", "Germany", "Greece", "Japan", "Hong Kong SAR, China"]
    chart_data = []
    for name in top_countries:
        pts = sorted([d for d in filtered if d["countryName"] == name], key=lambda x: x["year"])
        if not pts:
            continue
        label = "Hong Kong" if name == "Hong Kong SAR, China" else name
        series = [{"y": p["year"], "v": round(p["value"] / 1e6, 1)} for p in pts]
        chart_data.append({"n": label, "pts": series})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
