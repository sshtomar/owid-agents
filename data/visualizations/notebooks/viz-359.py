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
        # Old-Age Dependency Ratio, 1960–2024 — Methodology

        Trend lines showing the number of people aged 65+ per 100 working-age adults
        (ages 15–64). Reveals Japan's extreme aging trajectory and the divergence between
        rapidly aging East Asia and still-young South/Sub-Saharan Asia.
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
    from collections import defaultdict
    by_country = defaultdict(dict)
    for p in data:
        if p["value"] is not None:
            by_country[p["countryName"]][p["year"]] = p["value"]

    targets = ["Japan","Italy","Germany","France","Korea, Rep.","China","Brazil","India"]
    series = []
    for country in targets:
        if country not in by_country:
            print(f"MISSING: {country}")
            continue
        pts = sorted(by_country[country].items())
        name_short = country.replace("Korea, Rep.", "Korea")
        vals = [round(v, 1) for _, v in pts]
        y0 = pts[0][0]
        print(f"{name_short}: {y0}-{pts[-1][0]}, n={len(pts)}, latest={vals[-1]}%")
        series.append({"n": name_short, "s": vals, "y0": y0})

    return by_country, series, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — 64-year sweep shows demographic transition clearly
        - **Country selection**: Japan (extreme outlier), Europe (France, Germany, Italy),
          East Asia (Korea, China) transitioning fast, South America (Brazil) moderate,
          and India (still young)
        - **Time range**: 1960–2024 (65 data points, annual)
        - **Value range**: 0–56% (Japan hits 50.7% in 2024)
        - **Annotation**: Dot where Japan crosses 50% (around 2022)
        - **Key insights**:
          - Japan at 50.7%: more retirees than workers relative to the workforce
          - Korea rose from 5.6% to 27.5% — fastest recent acceleration among the 8
          - China's one-child policy now visible as a steep rise from ~2010
          - India at 10.5% remains among the world's youngest major economies
        """
    )
    return


@app.cell
def _(json, series):
    print(json.dumps(series, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
