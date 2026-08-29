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
        # Freshwater Key Biodiversity Areas Protected -- Methodology

        Documents the data pipeline behind viz-361.
        Source: sdg--15-1-2--ER_PTD_FRHWTR (UN SDG, 2000-2025)

        Shows the step-function nature of biodiversity protection commitments.
        Countries are sorted by 2025 protection level.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--15-1-2--ER_PTD_FRHWTR.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    selected = [
        "Croatia", "Dominican Republic", "Algeria", "Bulgaria", "Slovenia",
        "Cuba", "Albania", "Bosnia and Herzegovina", "Comoros",
        "El Salvador", "Seychelles", "Afghanistan", "Mali",
        "Brazil", "India", "China", "United States of America",
        "Kenya", "South Africa", "Australia"
    ]
    pts = {}
    for p in data:
        if p["countryName"] in selected and p["value"] is not None:
            if p["countryName"] not in pts:
                pts[p["countryName"]] = {}
            pts[p["countryName"]][p["year"]] = p["value"]

    series = []
    for c in selected:
        if c in pts:
            years_vals = sorted(pts[c].items())
            s = [round(v, 1) for _, v in years_vals]
            y0 = years_vals[0][0]
            v_end = years_vals[-1][1]
            series.append({"n": c, "s": s, "y0": y0, "l": round(v_end, 1)})
    series.sort(key=lambda x: x["l"], reverse=True)
    print(json.dumps(series, separators=(",", ":")))
    return pts, series, selected


if __name__ == "__main__":
    app.run()
