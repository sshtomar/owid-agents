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
        # Fossil Fuel Energy Share Slope Chart — Methodology

        Documents the data pipeline for viz-361: slope chart comparing fossil fuel
        energy consumption share in 1990 versus 2014 for 14 selected countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-COMM-FO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = [
        "Iceland", "Estonia", "Finland", "Austria", "France", "Germany",
        "Colombia", "Australia", "Japan", "China", "Iran, Islamic Rep.",
        "Cuba", "Canada", "Brazil"
    ]
    label_map = {"Iran, Islamic Rep.": "Iran"}

    out = []
    for name in selected:
        v90 = next((round(r["value"], 1) for r in data if r["countryName"] == name and r["year"] == 1990 and r["value"] is not None and r["value"] > 0), None)
        v14 = next((round(r["value"], 1) for r in data if r["countryName"] == name and r["year"] == 2014 and r["value"] is not None and r["value"] > 0), None)
        if v90 is not None and v14 is not None:
            label = label_map.get(name, name)
            out.append({"n": label, "a": v90, "b": v14})

    out.sort(key=lambda x: x["b"])
    for c in out:
        chg = c["b"] - c["a"]
        print(f"  {c['n']}: {c['a']}% -> {c['b']}%  ({'+' if chg>=0 else ''}{chg:.1f} pp)")
    return (out,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows 1990-to-2014 shift clearly for each country
        - **Country selection**: Spans the spectrum from near-zero fossil (Iceland via geothermal/hydro) to near-100% (Iran). Chosen for story diversity: European improvers, stagnant high users, and surprising movers (Cuba's surge, Japan's post-Fukushima climb)
        - **Time range**: 1990 vs 2014 — data quality is good for both endpoints; 2014 is the last year with broad coverage
        - **Color**: Green for decreasers, orange/red for large increases
        - **Highlights**: Estonia dropped 24pp (post-Soviet de-industrialisation + Baltic renewables); Japan climbed 10pp after nuclear shutdown; China surged 15pp as coal-driven growth accelerated
        """
    )
    return


@app.cell
def _(json, out):
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
