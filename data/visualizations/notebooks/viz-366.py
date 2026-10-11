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
        # Crude Death Rate: 1990 vs. 2022 — Methodology

        Slope chart comparing death rates at two points in time. The story has two opposing forces:
        aging in Europe pushing rates up, and health improvements in the developing world pulling rates down.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-CDRT-IN.json"
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

    TARGET = ["BG", "HR", "HU", "GR", "JP", "DE", "IT",
              "BR", "ID", "CN", "KE", "IN", "ET", "BD", "DZ", "IQ"]

    pairs = []
    for c in TARGET:
        rows = by_c.get(c, [])
        r1990 = [r for r in rows if r["y"] == 1990]
        r2022 = [r for r in rows if r["y"] == 2022]
        if r1990 and r2022:
            pairs.append({
                "n": r1990[0]["n"],
                "a": round(r1990[0]["v"], 1),
                "b": round(r2022[0]["v"], 1)
            })
            print(f"{r1990[0]['n']}: {r1990[0]['v']:.1f} -> {r2022[0]['v']:.1f} ({r2022[0]['v']-r1990[0]['v']:+.1f})")
    return TARGET, by_c, defaultdict, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — directly shows before/after change for each country
        - **Year selection**: 1990 (pre-post-Cold-War baseline) vs. 2022 (most recent complete year)
        - **Color**: Diverging by change magnitude — red for aging-driven increases, green for health-driven declines
        - **Country selection**: Mix of Eastern European aging economies and developing world success stories
        """
    )
    return


@app.cell
def _(json, pairs):
    import json as _json
    result = sorted(pairs, key=lambda x: -x["b"])
    print(_json.dumps(result, separators=(",", ":")))
    return
