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
        # Energy Use per Capita -- Methodology

        Documents the data pipeline for viz-359: trend lines showing energy
        consumption per capita (kg of oil equivalent) across economies at
        different income levels, 1990-2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SELECTED = {
        "Canada": "Canada", "Korea, Rep.": "South Korea",
        "Germany": "Germany", "Japan": "Japan", "France": "France",
        "China": "China", "Brazil": "Brazil", "India": "India"
    }

    pts = [d for d in data if d["value"] is not None and d["countryName"] in SELECTED]
    print(f"Filtered to {len(pts)} data points across {len(SELECTED)} countries")
    return SELECTED, pts


@app.cell
def _(SELECTED, pts):
    countries = {name: {} for name in SELECTED.values()}
    for p in pts:
        name = SELECTED[p["countryName"]]
        countries[name][p["year"]] = round(p["value"], 0)

    years = list(range(1990, 2025))
    chart_data = []
    for orig, name in SELECTED.items():
        yv = countries.get(name, {})
        series = [yv.get(y) for y in years]
        while series and series[-1] is None:
            series.pop()
        chart_data.append({"n": name, "s": series, "y0": 1990, "step": 1})

    chart_data.sort(key=lambda x: (x["s"][-1] or 0), reverse=True)
    for c in chart_data:
        print(f"{c['n']}: latest={c['s'][-1]:,.0f} kgoe, from 1990")
    return chart_data, countries, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- reveals divergence between high and low energy consumers
        - **Country selection**: 8 countries covering the full income spectrum
        - **Time range**: 1990-2023 captures post-Cold War energy transitions
        - **Highlights**: Canada and South Korea remain high consumers; Germany, France, Japan declining;
          China rising sharply from very low base; India still extremely low per capita
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
