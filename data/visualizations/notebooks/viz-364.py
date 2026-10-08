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
        # Arable Land per Person: A Shrinking Resource -- Methodology

        Documents the data pipeline behind viz-364.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-LND-ARBL-HA-PC.json"
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
                  "Caribbean", "Central Europe", "Heavily", "Fragile", "Small states",
                  "World", "OECD", "Pacific", "Middle East", "Low &", "Early-",
                  "Late-", "Post-", "Pre-", "High income", "Low income",
                  "Lower middle", "Upper middle"]
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
    selected_names = [
        "Jordan", "Chile", "Botswana", "Honduras", "Afghanistan", "Iraq",
        "Algeria", "Iran, Islamic Rep.", "Angola", "Cameroon", "Kenya",
        "Bangladesh", "Indonesia", "India", "China", "Cambodia",
        "Cote d'Ivoire", "Canada", "France", "Denmark", "Australia",
        "Argentina", "Bulgaria"
    ]
    result = []
    for c in selected_names:
        if c not in c_data:
            continue
        pts = c_data[c]
        yrs = [y for y in range(1970, 2023) if y in pts]
        if len(yrs) < 20:
            continue
        vals = [round(pts[y], 4) for y in yrs]
        pct = round((vals[-1] - vals[0]) / vals[0] * 100) if vals[0] > 0 else 0
        result.append({"n": c, "s": vals, "e": round(vals[0], 3), "l": round(vals[-1], 3), "y0": yrs[0], "pct": pct})
    result.sort(key=lambda x: x["pct"])
    print(f"Selected {len(result)} countries")
    for r in result[:5]:
        print(f"  {r['n']}: {r['e']:.3f} -> {r['l']:.3f} ({r['pct']}%)")
    return result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — compact view of 24 country trends simultaneously
        - **Sort order**: Biggest % declines first (bottom-left to top-right)
        - **Time range**: 1970-2022, annual data where available
        - **Story**: Nearly universal decline; Jordan -90%, Chile/Botswana -83%; only Bulgaria shows slight increase
        - **Color**: Each sparkline colored by magnitude of decline (warm=large decline, cool=stable)
        - **Interactivity**: Per-cell crosshair showing year and exact value
        """
    )
    return


if __name__ == "__main__":
    app.run()
