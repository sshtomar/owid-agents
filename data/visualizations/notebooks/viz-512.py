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
        # Bank Branch Counts: Digital Transformation vs. Financial Expansion -- Methodology

        Slope chart comparing commercial bank branches per 100,000 adults in 2004 vs 2022.
        Shows two diverging stories: branch closures in digitally-advanced economies and
        expansion in countries building financial infrastructure.
        Source: World Bank indicator FB.CBK.BRCH.P5.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FB-CBK-BRCH-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    skip = [
        "income", "World", "OECD", "IDA", "IBRD", "East", "South", "North",
        "Europe", "Caribbean", "Pacific", "Saharan", "dividend", "island",
        "Fragile", "developing", "Least", "Central", "emerging", "advanced",
        "Arab", "Euro", "Asia", "Africa", "Middle", "Western", "Eastern",
        "Latin", "small", "HIPC", "low", "high", "lower", "upper"
    ]

    candidates = []
    for c, yrs in by_country.items():
        if any(x.lower() in c.lower() for x in skip):
            continue
        early_y = next((y for y in sorted(yrs) if 2004 <= y <= 2006), None)
        late_y = next((y for y in sorted(yrs, reverse=True) if 2020 <= y <= 2024), None)
        if early_y and late_y:
            candidates.append({
                "n": c,
                "a": round(yrs[early_y], 1),
                "b": round(yrs[late_y], 1),
            })

    candidates.sort(key=lambda x: x["b"] - x["a"])
    print(f"Candidate countries: {len(candidates)}")
    return by_country, candidates, skip


@app.cell
def _(candidates):
    # Select ~20 countries: 10 biggest decliners + 10 biggest gainers
    decliners = [c for c in candidates if c["b"] - c["a"] < 0][:10]
    gainers = [c for c in candidates if c["b"] - c["a"] > 0][-10:]
    chart_data = decliners + gainers
    for d in chart_data:
        print(f"  {d['n']}: {d['a']} -> {d['b']} ({d['b']-d['a']:+.1f})")
    print(f"\nTotal: {len(chart_data)} countries")
    return chart_data, decliners, gainers


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- best for before/after comparison across many entities
        - **Country selection**: 10 largest decliners (digital disruption) + 10 largest gainers
          (financial inclusion expansion)
        - **Time points**: 2004 (earliest reliable) vs 2022 (most recent)
        - **Highlights**: Iceland lost 70 branches per 100k; Bolivia gained 59.
          Two fundamentally different dynamics in the same 18-year window.
        """
    )
    return


@app.cell
def _(json, chart_data):
    import json as _json
    print(_json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
