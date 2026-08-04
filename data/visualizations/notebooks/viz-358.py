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
        # Adult Female Mortality Rate, 1960–2024 — Methodology

        Trend lines showing the dramatic decline in adult female mortality
        across 10 diverse countries, from 1960 to 2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-AMRT-FE.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {raw['meta']['title']}")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict
    exclude_kw = [
        "IDA", "IBRD", "Sub-Saharan", "Least", "Heavily", "Low income",
        "Lower middle", "Africa Eastern", "Africa Western", "dividend",
        "Fragile", "World", "Upper middle", "East Asia", "South Asia",
        "Latin America", "Middle East", "Europe", "Central Asia",
        "Arab World", "Caribbean", "Pacific", "North America", "OECD",
        "Euro area", "demographic", "developing", "small states", "High income",
        "Post-demographic", "Central Europe", "European Union", "Middle income",
    ]
    by_country = defaultdict(list)
    for r in data:
        name = r["countryName"]
        if any(kw.lower() in name.lower() for kw in exclude_kw):
            continue
        if r["value"] is None:
            continue
        by_country[name].append((r["year"], r["value"]))
    print(f"Country count: {len(by_country)}")
    return (by_country,)


@app.cell
def _(by_country):
    selected_raw = {
        "Japan": "Japan",
        "Korea, Rep.": "South Korea",
        "China": "China",
        "Iran, Islamic Rep.": "Iran",
        "India": "India",
        "Bangladesh": "Bangladesh",
        "Ethiopia": "Ethiopia",
        "Brazil": "Brazil",
        "Gambia, The": "Gambia",
        "Ghana": "Ghana",
    }
    chart_data = []
    for raw_name, display_name in selected_raw.items():
        series = dict(by_country.get(raw_name, []))
        pts = []
        for yr in range(1960, 2025, 4):
            if yr in series:
                pts.append({"y": yr, "v": round(series[yr], 1)})
        if pts:
            chart_data.append({"n": display_name, "pts": pts})
            print(f"{display_name}: {pts[0]} -> {pts[-1]}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows change over 64-year span
        - **Country selection**: Asia-Pacific, South Asia, Sub-Saharan Africa, Latin America
        - **Story**: South Korea had the most dramatic decline (300→20); Gambia and Ghana still lag
        - **Cambodia excluded**: 1976 data point is a statistical outlier (Khmer Rouge era)
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
