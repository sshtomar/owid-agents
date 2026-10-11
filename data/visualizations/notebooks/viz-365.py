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
        # Child Wasting Prevalence — Methodology

        Horizontal bar chart of countries with the highest child wasting rates.
        Uses the most recent available year per country (all 2015 or later).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-WAST-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_c = defaultdict(list)
    for r in data:
        if r.get("value") is not None:
            by_c[r["country"]].append({"y": r["year"], "v": r["value"], "n": r["countryName"]})

    EXCLUDE = {"South Asia", "Lower middle income", "Low income",
               "Sub-Saharan Africa", "Africa Eastern and Southern",
               "Africa Western and Central", "Least developed countries: UN classification"}
    latest = []
    for c, rows in by_c.items():
        if len(c) != 2:
            continue
        rows_s = sorted(rows, key=lambda x: x["y"], reverse=True)
        r = rows_s[0]
        if r["y"] >= 2015 and r["n"] not in EXCLUDE:
            latest.append({"c": c, "n": r["n"], "y": r["y"], "v": round(r["v"], 1)})

    latest.sort(key=lambda x: -x["v"])
    print("Top 12 countries:")
    for r in latest[:12]:
        print(f"  {r['n']}: {r['v']}% ({r['y']})")
    return EXCLUDE, by_c, defaultdict, latest


@app.cell
def _(latest):
    chart_data = [{"n": r["n"], "v": r["v"], "y": r["y"]} for r in latest[:12]]
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar — clear ranking comparison across countries
        - **Filter**: Only individual countries (not regional aggregates); most recent year >= 2015
        - **Color**: Warm ramp by severity (>15%: accent red, >10%: orange, >8%: amber, else green)
        - **Reference line**: World average (6.6%) for context
        """
    )
    return


@app.cell
def _(json, chart_data):
    import json as _json
    print(_json.dumps(chart_data, separators=(",", ":")))
    return
