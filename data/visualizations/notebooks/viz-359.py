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
        # Natural Gas in the Power Mix — Methodology

        Trend lines showing the share of electricity generated from natural gas, 1990–2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NGAS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    countries = sorted(set(d["countryName"] for d in filtered if d["year"] == 2024))
    print(f"Countries with 2024 data: {len(countries)}")
    return countries, filtered


@app.cell
def _(filtered):
    selected = [("Israel", "Israel"), ("Argentina", "Argentina"), ("Ireland", "Ireland"),
                ("Italy", "Italy"), ("Greece", "Greece"), ("Japan", "Japan"),
                ("Korea, Rep.", "South Korea"), ("Germany", "Germany"), ("Finland", "Finland")]
    result = []
    for c_orig, c_display in selected:
        pts = {x["year"]: round(x["value"], 1) for x in filtered if x["countryName"] == c_orig}
        step_years = [y for y in range(1990, 2025, 2) if y in pts]
        if step_years:
            vals = [pts[y] for y in step_years]
            result.append({"n": c_display, "s": vals, "y0": step_years[0], "step": 2})
            print(f"{c_display}: 1990={pts.get(1990,'N/A')}, 2010={pts.get(2010,'N/A')}, 2024={pts.get(2024,'N/A')}")
    return result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 9 countries over 35 years with hover tooltips
        - **Country selection**: Mix of high-gas countries (Israel, Argentina, Ireland, Italy),
          medium-gas (Japan, South Korea, Germany), and one phasing-out (Finland)
        - **Story**: Israel's transformation is dramatic — from 0% in 1990 to ~70% by 2024 after
          major offshore gas discoveries (Tamar 2013, Leviathan 2019). Finland deliberately reduced
          gas as part of its clean-energy transition.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
