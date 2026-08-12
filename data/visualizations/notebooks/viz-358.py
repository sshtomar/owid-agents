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
        # Anemia Among Non-Pregnant Women, 2000 vs 2022 — Methodology

        Documents the data pipeline for viz-358.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-ANM-NPRG-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_keywords = ["Eastern","Western","Central","Arab","Caribbean","Euro","Middle","Africa","Sub-Saharan","Latin","South Asia","Pacific","World","OECD","income","IDA","IBRD","dividend","debt","blend","Fragile","Small","Least","heavily","depopulated","Other","region","global","International"]
    by_country = {}
    for p in data:
        if p["value"] is None:
            continue
        c = p["countryName"]
        if any(x.lower() in c.lower() for x in skip_keywords):
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][p["year"]] = p["value"]
    print(f"Individual countries: {len(by_country)}")
    return (by_country,)


@app.cell
def _(by_country):
    slope_data = []
    for c, yrs in by_country.items():
        a = yrs.get(2000)
        b = yrs.get(2022) or yrs.get(2021) or yrs.get(2020)
        if a is not None and b is not None:
            slope_data.append({"n": c, "a": round(a, 1), "b": round(b, 1)})

    slope_data.sort(key=lambda x: x["b"], reverse=True)
    print(f"Countries with both endpoints: {len(slope_data)}")
    values_2022 = [s["b"] for s in slope_data]
    print(f"2022 range: {min(values_2022):.1f}% – {max(values_2022):.1f}%")
    return (slope_data,)


@app.cell
def _(slope_data):
    top_burden = slope_data[:8]
    improvers = sorted(slope_data, key=lambda x: x["b"] - x["a"])[:5]
    low_burden = [s for s in slope_data if s["b"] < 20][-6:]

    selected = {}
    for s in top_burden + improvers + low_burden:
        selected[s["n"]] = s

    result = sorted(selected.values(), key=lambda x: x["b"], reverse=True)
    print(f"Final country set: {len(result)}")
    return (result,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares two time points across many countries
        - **Country selection**: Top-burden countries, biggest improvers, and low-burden countries for contrast
        - **Year pair**: 2000 (pre-MDG baseline) vs 2022 (most recent)
        - **Color**: Red = worsened, amber = stable, green = improved
        - **Highlights**: Afghanistan worsened significantly; Sub-Saharan Africa still >40%; Guatemala made the biggest improvement
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
