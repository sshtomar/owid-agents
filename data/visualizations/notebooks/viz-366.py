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
        # TB Treatment Success: Progress With a Paradox -- Methodology

        Documents the data pipeline behind viz-366.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-TBS-CURE-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [r for r in data if r["value"] is not None]
    skip_words = ["income", "IDA", "IBRD", "Africa Eastern", "Africa Western",
                  "Arab World", "East Asia", "South Asia", "Europe &", "Euro area",
                  "European", "Latin America", "North America", "Sub-Saharan",
                  "Caribbean", "Central Europe", "Heavily", "Fragile",
                  "Small states", "World", "OECD", "Pacific", "Middle East",
                  "Low &", "Early-", "Late-", "Post-", "Pre-",
                  "High income", "Low income", "Lower middle", "Upper middle"]
    c_data = {}
    for r in filtered:
        c = r["countryName"]
        if any(s in c for s in skip_words):
            continue
        if c not in c_data:
            c_data[c] = {}
        c_data[c][r["year"]] = r["value"]
    print(f"Individual countries: {len(c_data)}")
    return c_data, filtered


@app.cell
def _(c_data, json):
    pairs = []
    for c, pts in c_data.items():
        if 2005 not in pts:
            continue
        best_y = None
        for yr in [2022, 2021, 2020]:
            if yr in pts:
                best_y = yr
                break
        if best_y is None:
            continue
        v2005 = pts[2005]
        v_recent = pts[best_y]
        if v2005 == 0 or v_recent == 0:
            continue
        change = round(v_recent - v2005, 1)
        pairs.append({"n": c, "a": round(v2005, 1), "b": round(v_recent, 1), "change": change})
    pairs.sort(key=lambda x: x["change"])
    selected_names = [
        "Congo, Rep.", "Eswatini", "Bahamas, The", "Ghana",
        "Congo, Dem. Rep.", "Central African Republic", "Burundi",
        "Cambodia", "Bangladesh", "China", "Ethiopia", "Kenya",
        "India", "Indonesia", "Brazil", "Ecuador",
        "Iceland", "Germany", "Bosnia and Herzegovina", "Bahrain", "Denmark"
    ]
    selected = [p for p in pairs if p["n"] in selected_names]
    print(f"Selected {len(selected)} countries")
    for s in selected:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['change']:+.1f})")
    return pairs, selected, selected_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — 2005 vs 2022 before/after comparison
        - **Countries**: 21 countries spanning big improvers, stable performers, and surprising decliners
        - **Story**: Congo Rep. and Eswatini improved dramatically (+50, +47 pts); Denmark fell from 85% to 18%
        - **Paradox**: European/wealthy countries with low TB incidence see declining success rates,
          possibly because MDR-TB is more common among cases, or patients are lost to follow-up more easily
        - **Color**: Deep green = large improvement, orange/red = large decline
        """
    )
    return


if __name__ == "__main__":
    app.run()
