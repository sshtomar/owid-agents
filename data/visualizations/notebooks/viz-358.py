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
        # Energy Use per Capita, 1990–2022 — Methodology

        Trend lines showing total primary energy use per person (kg of oil equivalent)
        for 8 countries spanning the income spectrum. Reveals the vast gap between
        rich and poor nations, and China's dramatic catch-up to Western levels.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(dict)
    for p in data:
        if p["value"] is not None:
            by_country[p["countryName"]][p["year"]] = p["value"]

    targets = ["Canada","Korea, Rep.","Germany","China","Brazil","India","Bangladesh","Chad"]
    series = []
    for country in targets:
        if country not in by_country:
            print(f"MISSING: {country}")
            continue
        pts = sorted(by_country[country].items())
        # Trim to 1990-2022
        pts = [(y, v) for y, v in pts if 1990 <= y <= 2022]
        name_short = country.replace("Korea, Rep.", "Korea")
        vals = [round(v) for _, v in pts]
        y0 = pts[0][0]
        print(f"{name_short}: {y0}-{pts[-1][0]}, n={len(pts)}, 2022={vals[-1]}")
        series.append({"n": name_short, "s": vals, "y0": y0})

    return by_country, series, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — best for showing divergent trajectories across 3+ decades
        - **Country selection**: Spans income distribution (Canada/Korea at top, Chad at bottom)
          with China as the key story of rapid industrialization
        - **Time range**: 1990–2022, 33 annual data points per country
        - **Value range**: 0–9,000 kg oil eq (excludes Iceland at 16,000 which would compress others)
        - **Key insights**:
          - Canada flat at ~8,000; Korea rose 2.5x from 2,000 to 5,400
          - Germany declined ~35% (efficiency gains, deindustrialization)
          - China rose 3.5x, nearing Germany and Brazil
          - India and Bangladesh slowly rising; Chad declining slightly
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
