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
        # Family Planning Access -- Methodology

        Slope chart of women aged 15-49 with family planning needs satisfied
        by modern methods, comparing ~2000 vs ~2021-2022 across 16 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--SDGFPALL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso3_map = {
        "ETH": "Ethiopia", "BEN": "Benin", "BFA": "Burkina Faso", "NGA": "Nigeria",
        "KHM": "Cambodia", "GHA": "Ghana", "MDG": "Madagascar", "UGA": "Uganda",
        "MOZ": "Mozambique", "PHL": "Philippines", "KEN": "Kenya", "NPL": "Nepal",
        "JOR": "Jordan", "VNM": "Vietnam", "SLV": "El Salvador", "JAM": "Jamaica",
    }
    from collections import defaultdict
    by_country = defaultdict(list)
    for p in data:
        code = p["country"]
        if code in iso3_map and p["value"] is not None:
            by_country[iso3_map[code]].append({"y": p["year"], "v": p["value"]})

    result = []
    for c, pts in by_country.items():
        pts.sort(key=lambda x: x["y"])
        early = [p for p in pts if p["y"] <= 2003]
        late = [p for p in pts if p["y"] >= 2020]
        if early and late:
            result.append({"n": c, "a": round(early[0]["v"], 1), "b": round(late[-1]["v"], 1)})

    result.sort(key=lambda x: x["a"])
    print(f"Countries with before/after: {len(result)}")
    for r in result:
        chg = r["b"] - r["a"]
        print(f"  {r['n']}: {r['a']}% -> {r['b']}% ({'+' if chg>=0 else ''}{chg:.1f})")
    return by_country, iso3_map, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — before/after comparison across countries
        - **Country selection**: Low and middle income countries from Sub-Saharan Africa, South/SE Asia, Latin America
        - **Time range**: ~2000 (baseline) vs ~2021-2022 (latest)
        - **Color**: Green for large gains, amber for moderate, red for decline
        - **Highlights**: Ethiopia 15%→61% (dramatic gain); Kenya 48%→79%; Jordan and El Salvador slight reversal
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
