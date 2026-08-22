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
        # International Migrant Stock Slope Chart — Methodology

        Documents the data pipeline for viz-360: slope chart comparing foreign-born
        population share in 1990 versus 2020 across selected countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SM-POP-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = [
        "Bahrain", "Jordan", "Australia", "Canada", "Israel", "Germany",
        "Ireland", "Austria", "Iceland", "Belgium", "France", "Denmark",
        "Greece", "Estonia", "Djibouti", "Equatorial Guinea", "Gabon", "Belize"
    ]

    out = []
    for name in selected:
        v90 = next((r["value"] for r in data if r["countryName"] == name and r["year"] == 1990 and r["value"] is not None), None)
        v20 = next((r["value"] for r in data if r["countryName"] == name and r["year"] == 2020 and r["value"] is not None), None)
        if v90 is not None and v20 is not None:
            out.append({"n": name, "a": round(v90, 1), "b": round(v20, 1)})

    out.sort(key=lambda x: x["b"], reverse=True)
    for c in out:
        chg = c["b"] - c["a"]
        print(f"  {c['n']}: {c['a']}% -> {c['b']}%  ({'+' if chg>=0 else ''}{chg:.1f} pp)")
    return (out,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — best shows direction and magnitude of change for many entities simultaneously
        - **Country selection**: Mix of Gulf states (labour migration), traditional immigration nations (Australia, Canada), European transformers (Iceland, Ireland), and declining migrant-share nations (Israel, Estonia)
        - **Time range**: 1990 vs 2020 — bookends the era of globalisation
        - **Color**: Warm (large increase) to cool (decrease), encoded by pp change
        - **Highlights**: Bahrain jumped 19pp; Israel fell 12pp as Soviet immigrants naturalised; Iceland transformed from 4% to 18%
        """
    )
    return


@app.cell
def _(json, out):
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
