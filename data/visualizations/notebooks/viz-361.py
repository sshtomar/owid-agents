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
    # HIV Incidence in Sub-Saharan Africa — Methodology

    Trend lines for 8 countries with the highest peak HIV incidence rates, showing the
    dramatic decline from catastrophic peaks in the 1990s to near-control by 2024.
    Botswana and Eswatini peaked at 50 new infections per 1,000 uninfected people per year.
    """)
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-HIV-INCD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} points")
    return data, raw


@app.cell
def _(data, json):
    points = [r for r in data if r["value"] is not None]
    by_country = {}
    for r in points:
        c = r["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][r["year"]] = r["value"]

    focus = ["Eswatini", "Botswana", "Kenya", "Cote d'Ivoire",
             "Central African Republic", "Burundi", "Cameroon", "Ethiopia"]
    years = list(range(1990, 2025))

    result = []
    for c in focus:
        if c not in by_country:
            print(f"MISSING: {c}")
            continue
        yd = by_country[c]
        pts = [{"y": y, "v": round(yd[y], 2)} for y in years if y in yd]
        result.append({"n": c, "pts": pts})
        print(f"{c}: peak={max(yd.values()):.2f}, latest={yd[max(yd.keys())]:.2f}")

    print(json.dumps(result, separators=(",", ":")))
    return (result,)


if __name__ == "__main__":
    app.run()
