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
        # Energy Use per Capita — Methodology

        Slope chart comparing kg of oil equivalent per person in 1990 vs 2023 for 15 countries.
        Shows divergence between European efficiency gains and developing-economy growth.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    countries = {}
    for p in data:
        c = p["countryName"]
        if p["value"] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][p["year"]] = p["value"]
    return (countries,)


@app.cell
def _(countries):
    mapping = {
        "Iceland": "Iceland", "Canada": "Canada", "Korea, Rep.": "South Korea",
        "Australia": "Australia", "Finland": "Finland", "Belgium": "Belgium",
        "Germany": "Germany", "France": "France", "Japan": "Japan",
        "China": "China", "Brazil": "Brazil", "Egypt, Arab Rep.": "Egypt",
        "Indonesia": "Indonesia", "India": "India", "Bangladesh": "Bangladesh"
    }
    chart_data = []
    for orig, display in mapping.items():
        if orig not in countries:
            continue
        vals = countries[orig]
        v90 = vals.get(1990)
        v23 = vals.get(2023) or vals.get(2022)
        if not v90 or not v23:
            continue
        v90, v23 = round(v90), round(v23)
        pct = round((v23 / v90 - 1) * 100)
        chart_data.append({"n": display, "a": v90, "b": v23, "pct": pct})
    chart_data.sort(key=lambda x: -x["a"])
    print("Country, 1990, 2023, pct_change:")
    for d in chart_data:
        print(f"  {d['n']}: {d['a']:,} -> {d['b']:,} ({d['pct']:+d}%)")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — best for comparing values at two time points across many entities
        - **Year selection**: 1990 (post-Soviet baseline) vs 2023 (latest consistent data)
        - **Color**: Green for decrease (efficiency improvement), orange/red for large increases
        - **Highlights**: South Korea +156%, China +269% from very low bases; Germany -34%
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
