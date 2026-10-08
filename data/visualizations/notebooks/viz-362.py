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
        # Intentional Homicides: Two Decades of Change -- Methodology

        Documents the data pipeline behind viz-362.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
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
                  "Caribbean small", "Central Europe", "Heavily", "Fragile",
                  "Small states", "World", "OECD"]
    country_data = {}
    for r in filtered:
        c = r["countryName"]
        if any(s in c for s in skip_words):
            continue
        if c not in country_data:
            country_data[c] = {}
        country_data[c][r["year"]] = r["value"]
    print(f"Individual countries: {len(country_data)}")
    return country_data, filtered


@app.cell
def _(country_data):
    pairs = []
    for c, pts in country_data.items():
        if 2000 not in pts:
            continue
        best_y = None
        for yr in [2023, 2022, 2021, 2020]:
            if yr in pts:
                best_y = yr
                break
        if best_y is None:
            continue
        pairs.append({"n": c, "a": round(pts[2000], 2), "b": round(pts[best_y], 2)})
    pairs.sort(key=lambda x: -x["a"])
    selected = pairs[:22]
    print(f"Selected {len(selected)} countries by 2000 rate")
    for p in selected:
        print(f"  {p['n']}: {p['a']} -> {p['b']}")
    return pairs, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows before/after comparison dramatically
        - **Countries**: Top 22 by 2000 homicide rate; captures Latin American crisis + improvement stories
        - **Years**: 2000 vs most recent (2020-2023) — two full decades of change
        - **Highlights**: Colombia and El Salvador dropped from ~60-68 to under 25; Ecuador surged from 14 to 46
        - **Color**: Red=increase, green=decrease, grey=stable
        """
    )
    return


@app.cell
def _(json, selected):
    import json as _json
    print(_json.dumps(selected, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
