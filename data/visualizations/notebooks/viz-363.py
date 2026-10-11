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
        # HIV New Infections in Sub-Saharan Africa — Methodology

        Trend lines chart showing new HIV infections per 1,000 uninfected people ages 15–49.
        Focuses on six Sub-Saharan African countries with the most dramatic stories.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-HIV-INCD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    TARGET = {"SZ": "Eswatini", "BW": "Botswana", "KE": "Kenya",
              "CF": "Central African Rep.", "BI": "Burundi",
              "ET": "Ethiopia", "ZG": "Sub-Saharan Africa"}
    by_c = defaultdict(list)
    for r in data:
        if r.get("value") is not None and r["country"] in TARGET:
            by_c[r["country"]].append({"y": r["year"], "v": round(r["value"], 2)})
    print(f"Countries loaded: {len(by_c)}")
    for c, rows in by_c.items():
        rows_s = sorted(rows, key=lambda x: x["y"])
        peak = max(rows, key=lambda x: x["v"])
        print(f"  {TARGET[c]}: peak={peak['v']:.2f} ({peak['y']}), latest={rows_s[-1]['v']:.2f}")
    return TARGET, by_c, defaultdict


@app.cell
def _(by_c, TARGET):
    chart_data = []
    for c, name in TARGET.items():
        rows = sorted(by_c.get(c, []), key=lambda x: x["y"])
        rows_f = [r for r in rows if 1990 <= r["y"] <= 2024]
        s = [r["v"] for r in rows_f]
        chart_data.append({"n": name, "s": s, "y0": rows_f[0]["y"]})
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — reveals the epidemic arc (rise, peak, sustained decline)
        - **Y-axis**: Linear scale 0–55 per 1,000 captures both extreme peaks and near-zero current values
        - **Country selection**: Eswatini/Botswana (extreme cases), Kenya (dramatic success), Burundi/Ethiopia (fast decliners), CAR (slow decliner), Sub-Saharan Africa aggregate (regional context)
        - **Highlights**: Eswatini peaked at 50 per 1,000 in 1997; Kenya dropped 97%; the entire region improved 88%
        """
    )
    return


@app.cell
def _(json, chart_data):
    import json as _json
    print(_json.dumps(chart_data, separators=(",", ":")))
    return
