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

        Slope chart comparing 2000 vs 2024 GDP per person employed (constant 2021 PPP$)
        for 14 diverse countries. Shows the wide productivity gap and which countries
        are catching up fastest.
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
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    years = sorted(set(d["year"] for d in filtered))
    print(f"Year range: {years[0]}-{years[-1]}")
    print(f"Value range: ${min(values):,.0f} - ${max(values):,.0f}")
    return values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs 2024) — two-point comparison reveals trajectory
        - **Scale**: Log10 — spans two orders of magnitude ($2k to $235k); log compresses extreme outliers
        - **Country selection**: 14 countries across income levels and continents; excludes regional aggregates
        - **Color**: Encodes % growth — highlights developing economies' rapid productivity gains
        - **Notable**: Guyana's 7x gain driven by 2015 oil discovery; Ireland/France gain from MNC IP
        - **Highlights**: S. Korea +71%, China +510%, India +182%, Ethiopia +266% — vs Germany +11%
        """
    )
    return


@app.cell
def _(json):
    chart_data = [
        {"n": "Guyana", "a": 25117, "b": 204862},
        {"n": "France", "a": 114080, "b": 127332},
        {"n": "Germany", "a": 110739, "b": 123472},
        {"n": "Australia", "a": 95966, "b": 114528},
        {"n": "South Korea", "a": 57330, "b": 98259},
        {"n": "Japan", "a": 76595, "b": 84354},
        {"n": "Chile", "a": 47850, "b": 63924},
        {"n": "China", "a": 7508, "b": 45842},
        {"n": "Brazil", "a": 34062, "b": 41441},
        {"n": "Indonesia", "a": 13753, "b": 29217},
        {"n": "India", "a": 8662, "b": 24430},
        {"n": "Bolivia", "a": 17667, "b": 21296},
        {"n": "Bangladesh", "a": 7693, "b": 20763},
        {"n": "Ethiopia", "a": 1958, "b": 7173},
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
