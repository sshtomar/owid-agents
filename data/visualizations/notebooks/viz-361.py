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
        # Anemia Among Women of Reproductive Age — Methodology

        Documents the data pipeline behind viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-ALLW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_keywords = [
        "Africa", "Asia", "Europe", "America", "Pacific", "Arab", "Caribbean",
        "income", "World", "Central", "Eastern", "Western", "Northern", "Southern",
        "OECD", "Euro", "Fragile", "Heavily", "IBRD", "IDA", "Small", "dividend",
        "states", "countries", "area", "region", "demographic"
    ]
    individual = [
        d for d in data
        if d["value"] is not None
        and not any(k in d["countryName"] for k in agg_keywords)
    ]
    print(f"Individual country rows: {len(individual)}")
    return agg_keywords, individual


@app.cell
def _(individual):
    from collections import defaultdict
    country_data = defaultdict(dict)
    for row in individual:
        country_data[row["countryName"]][row["year"]] = row["value"]

    # Sort by 2023 value, take top 30
    latest_vals = {c: yd.get(2023) or yd.get(2022) for c, yd in country_data.items()}
    latest_vals = {c: v for c, v in latest_vals.items() if v is not None}
    top30 = sorted(latest_vals.items(), key=lambda x: -x[1])[:30]
    print("Top 30 by 2023 anemia rate:")
    for name, val in top30:
        print(f"  {name}: {val:.1f}%")
    return country_data, latest_vals, top30


@app.cell
def _(country_data, top30):
    import json
    years = list(range(2000, 2024))
    chart_data = []
    for name, _ in top30:
        yd = country_data[name]
        series = [round(yd.get(y) or 0, 1) for y in years]
        earliest = yd.get(2000) or yd.get(2001)
        latest = yd.get(2023) or yd.get(2022)
        if earliest and latest:
            chart_data.append({
                "n": name,
                "s": series,
                "e": round(earliest, 1),
                "l": round(latest, 1)
            })
    print(f"Final series: {len(chart_data)}")
    return chart_data, json, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — allows compact comparison of 30 countries
        - **Sorting**: By 2023 value (highest burden first)
        - **Color coding**: Country name turns red if anemia worsened by >2pp, green if improved by >2pp
        - **Key observations**:
          - India and Afghanistan are rising (worsening), not improving
          - West African countries (Benin, Gambia, Chad) have fallen from very high levels
            but remain above 45%
          - Gabon has persistently high rates (~60%) despite upper-middle income status
          - Bangladesh shows a U-curve: declined to 34% around 2010, now rising again to 37.6%
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
