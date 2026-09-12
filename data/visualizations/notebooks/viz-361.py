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
        # Labor Productivity — Methodology

        Trend lines for GDP per person employed (constant 2021 PPP $) across 10 countries, 1995-2020.
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
    PICKS = {'Germany', 'France', 'Japan', 'Australia', 'Canada',
             'Brazil', 'China', 'India', 'Bangladesh', 'Ethiopia'}

    by_country = {}
    for p in data:
        cn = p["countryName"]
        if cn not in PICKS:
            continue
        if p["value"] is None:
            continue
        if cn not in by_country:
            by_country[cn] = {}
        by_country[cn][p["year"]] = round(p["value"])

    print(f"Countries found: {list(by_country.keys())}")
    return by_country,


@app.cell
def _(by_country):
    years = list(range(1995, 2021, 5))
    chart_data = []
    for country, vals in by_country.items():
        s = [vals.get(y) for y in years]
        chart_data.append({"n": country, "s": s, "y0": years[0], "step": 5})

    chart_data.sort(key=lambda x: -(x["s"][-1] or 0))
    for c in chart_data:
        print(f"{c['n']}: {c['s'][0]:,} -> {c['s'][-1]:,}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows trajectory divergence over 25 years
        - **Country selection**: Representative mix: 5 high-income, 3 middle-income, 2 low-income
        - **Sampling**: Every 5 years (1995-2020) for clarity
        - **Highlights**: China's 7x surge, convergence of India/Bangladesh, Ethiopia's rapid gains from tiny base
        - **Scale**: Linear; high-income countries plateau near top, creates a clear visual tier structure
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
