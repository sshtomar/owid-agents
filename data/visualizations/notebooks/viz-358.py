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
        # Old-Age Dependency Ratio — Methodology

        Trend lines showing how the old-age dependency ratio (people 65+ per 100 working-age adults)
        evolved from 1960 to 2024 across nine countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    return countries, filtered, years


@app.cell
def _(filtered):
    selected = ["Japan", "Germany", "Italy", "France", "Korea, Rep.", "China", "Brazil", "India", "Indonesia"]
    result = []
    for c in selected:
        pts = {x["year"]: x["value"] for x in filtered if x["countryName"] == c}
        step_years = [y for y in range(1960, 2025, 5) if y in pts]
        if not step_years:
            print(f"No data for {c}")
            continue
        vals = [round(pts[y], 1) for y in step_years]
        display = c.replace("Korea, Rep.", "South Korea")
        result.append({"n": display, "s": vals, "y0": step_years[0], "step": 5})
        print(f"{c}: 1960={pts.get(1960,'N/A'):.1f}, 2000={pts.get(2000,'N/A'):.1f}, 2024={pts.get(2024,'N/A'):.1f}")
    return result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows long-run evolution with hover interactivity
        - **Countries**: 9 countries across 4 continents, chosen for geographic diversity and contrast
        - **Step**: Every 5 years to keep the data compact while showing the full trend
        - **Story**: Japan's ratio nearly sextupled (8.9 to 49.1) — no other country comes close.
          South Korea is on a steep upward trajectory. India and Indonesia remain very young.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
