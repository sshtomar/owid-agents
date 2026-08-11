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
    mo.md("""
    # Female to Male Labor Force Participation Ratio — Methodology

    Trend lines for 8 world regions showing the ratio of female to male labor force
    participation rate (%) from 1990 to 2024. 100 = full parity.
    Arab World stuck near 27–31%; Latin America improved from 53% to 69%.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-CACT-FM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} points")
    return data, raw


@app.cell
def _(data, json):
    points = [r for r in data if r["value"] is not None]
    by_entity = {}
    for r in points:
        c = r["countryName"]
        if c not in by_entity:
            by_entity[c] = {}
        by_entity[c][r["year"]] = r["value"]

    years = list(range(1990, 2025, 2))
    entities = [
        ("Arab World", "Arab World"),
        ("Sub-Saharan Africa", "Sub-Saharan Africa"),
        ("South Asia", "South Asia"),
        ("East Asia & Pacific", "East Asia & Pacific"),
        ("Latin America & Caribbean", "Latin America"),
        ("Europe & Central Asia", "Europe & C. Asia"),
        ("North America", "North America"),
        ("World", "World"),
    ]

    result = []
    for entity, label in entities:
        if entity not in by_entity:
            print(f"NOT FOUND: {entity}")
            continue
        yd = by_entity[entity]
        pts = [{"y": y, "v": round(yd[y], 1)} for y in years if y in yd]
        if pts:
            result.append({"n": label, "pts": pts})
            print(f"{label}: 1990={yd.get(1990, 'N/A'):.1f}, 2024={yd.get(2024, 'N/A'):.1f}")

    print(json.dumps(result, separators=(",", ":")))
    return (result,)


if __name__ == "__main__":
    app.run()
