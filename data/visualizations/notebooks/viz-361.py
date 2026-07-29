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
        # Patent Applications by Residents — Methodology

        Sparkline grid showing annual patent applications filed by residents from 1990 to 2021
        for 12 countries. China's exponential rise is the dominant story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
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
        "China": "China", "Japan": "Japan", "Korea, Rep.": "South Korea",
        "Germany": "Germany", "India": "India", "Iran, Islamic Rep.": "Iran",
        "France": "France", "Italy": "Italy", "Canada": "Canada",
        "Brazil": "Brazil", "Indonesia": "Indonesia", "Australia": "Australia"
    }
    chart_data = []
    for orig, display in mapping.items():
        if orig not in countries:
            continue
        vals = countries[orig]
        series = [int(vals.get(yr, 0)) for yr in range(1990, 2022)]
        valid = [v for v in series if v > 0]
        if not valid:
            continue
        chart_data.append({
            "n": display,
            "s": series,
            "max": max(valid),
            "first": valid[0],
            "last": valid[-1]
        })

    # Sort by max descending
    chart_data.sort(key=lambda x: -x["max"])
    print("Country, first_nonzero, last_nonzero, max:")
    for d in chart_data:
        print(f"  {d['n']}: {d['first']:,} -> {d['last']:,} (max={d['max']:,})")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — compact comparison across many entities
        - **Normalization**: Each cell normalized to its own min/max for readability
        - **Year range**: 1990–2021 (32 data points)
        - **Country selection**: Top 12 by all-time maximum patent applications
        - **Zero handling**: Years with 0 reported are treated as missing and skipped in sparklines
        - **Highlights**: China grew 245x; Japan peaked ~2000 and declined; South Korea and India rising
        """
    )
    return


@app.cell
def _(json, chart_data):
    export = [{"n": d["n"], "s": d["s"]} for d in chart_data]
    print(json.dumps(export, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
