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

        Trend lines chart on log scale showing the explosive growth of Chinese patent filings
        versus other major innovation economies.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    TARGET = {"CN": "China", "JP": "Japan", "KR": "South Korea", "DE": "Germany", "IN": "India", "FR": "France"}
    by_c = defaultdict(list)
    for r in data:
        if r.get("value") is not None and r["country"] in TARGET:
            by_c[r["country"]].append({"y": r["year"], "v": round(r["value"])})
    for c, name in TARGET.items():
        rows = sorted(by_c.get(c, []), key=lambda x: x["y"])
        rows_f = [r for r in rows if 1990 <= r["y"] <= 2024]
        print(f"{name}: {rows_f[0]['v']:,} (1990) -> {rows_f[-1]['v']:,} (2024)")
    return TARGET, by_c, defaultdict


@app.cell
def _(by_c, TARGET):
    chart_data = []
    for c, name in TARGET.items():
        rows = sorted(by_c.get(c, []), key=lambda x: x["y"])
        rows_f = [r for r in rows if 1990 <= r["y"] <= 2024]
        chart_data.append({"n": name, "s": [r["v"] for r in rows_f], "y0": 1990})
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with log scale — range spans 5k to 1.7M, requiring log scale
        - **Country selection**: The 5 largest patent-filing nations plus France for European context
        - **Highlights**: China's 287x growth since 1990; South Korea's 22x growth; Japan's plateau
        - **Key moment**: China crossed Japan in 2006, crossed the rest of the world combined around 2020
        """
    )
    return


@app.cell
def _(json, chart_data):
    import json as _json
    print(_json.dumps(chart_data, separators=(",", ":")))
    return
