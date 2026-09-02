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
        # Labor Productivity: GDP per Person Employed -- Methodology

        Documents the data pipeline for viz-358: trend lines showing GDP per
        person employed (constant 2021 PPP $) across economies at different
        income levels, 1991-2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-GDP-PCAP-EM-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SELECTED = {
        "Ireland": "Ireland", "Denmark": "Denmark", "Germany": "Germany",
        "France": "France", "Japan": "Japan", "Korea, Rep.": "South Korea",
        "China": "China", "Brazil": "Brazil", "India": "India",
        "Indonesia": "Indonesia", "Ethiopia": "Ethiopia"
    }

    pts = [d for d in data if d["value"] is not None and d["countryName"] in SELECTED]
    print(f"Filtered to {len(pts)} data points across {len(SELECTED)} countries")
    return SELECTED, pts


@app.cell
def _(SELECTED, pts):
    import statistics
    countries = {name: {} for name in SELECTED.values()}
    for p in pts:
        name = SELECTED[p["countryName"]]
        countries[name][p["year"]] = round(p["value"], 0)

    years = list(range(1991, 2025))
    chart_data = []
    for orig, name in SELECTED.items():
        yv = countries.get(name, {})
        series = [yv.get(y) for y in years]
        while series and series[-1] is None:
            series.pop()
        chart_data.append({"n": name, "s": series, "y0": 1991, "step": 1})

    chart_data.sort(key=lambda x: (x["s"][-1] or 0), reverse=True)
    for c in chart_data:
        print(f"{c['n']}: latest={c['s'][-1]:,.0f} PPP$, years of data={len([v for v in c['s'] if v])}")
    return chart_data, countries, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows diverging productivity trajectories over 33 years
        - **Country selection**: 11 countries spanning from Ethiopia (~7k) to Ireland (~230k) PPP$
        - **Time range**: 1991-2024 to capture post-Cold War globalization era
        - **Highlights**: Ireland's explosive growth (MNC accounting effects), China's 14x rise,
          persistent gap between rich and poor economies despite convergence in Asia
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
