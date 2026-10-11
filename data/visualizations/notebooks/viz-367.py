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
        # Income Share of the Top 10% — Methodology

        Slope chart comparing the richest decile's income share from the mid-1990s to 2022–2024.
        Shows the divergence between declining Latin American inequality and rising European inequality.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SI-DST-10TH-10.json"
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

    TARGET = {
        "CO": ("Colombia", 1996, 2024), "BR": ("Brazil", 1995, 2024),
        "HN": ("Honduras", 1995, 2024), "CL": ("Chile", 1996, 2024),
        "BO": ("Bolivia", 1997, 2024), "EC": ("Ecuador", 1995, 2024),
        "AR": ("Argentina", 1995, 2024),
        "BG": ("Bulgaria", 1995, 2023), "DK": ("Denmark", 1995, 2023),
        "DE": ("Germany", 1995, 2022),
        "ET": ("Ethiopia", 1995, 2021), "AM": ("Armenia", 1996, 2024),
        "CN": ("China", 1996, 2022), "IN": ("India", 2004, 2023),
        "ID": ("Indonesia", 1996, 2024), "IE": ("Ireland", 1995, 2023)
    }

    pairs = []
    for c, (name, ya_t, yb_t) in TARGET.items():
        rows = by_c.get(c, [])
        a_rows = sorted(rows, key=lambda x: abs(x["y"] - ya_t))
        b_rows = sorted(rows, key=lambda x: abs(x["y"] - yb_t))
        if a_rows and b_rows:
            a_r, b_r = a_rows[0], b_rows[0]
            pairs.append({"n": name, "a": round(a_r["v"], 1), "b": round(b_r["v"], 1)})
            print(f"{name}: {a_r['v']:.1f}% -> {b_r['v']:.1f}% ({b_r['v']-a_r['v']:+.1f}pp)")
    return TARGET, by_c, defaultdict, pairs


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — mid-1990s vs 2022–2024 captures 25+ years of distributional change
        - **Color**: Diverging — red/orange for rising inequality, green for falling
        - **Country selection**: LatAm dominated because data coverage is better; European comparators show contrasting trend
        - **Highlights**: Bolivia/Honduras/Chile showed large gains; Denmark/Bulgaria rising despite welfare states
        """
    )
    return


@app.cell
def _(json, pairs):
    import json as _json
    result = sorted(pairs, key=lambda x: -x["a"])
    print(_json.dumps(result, separators=(",", ":")))
    return
