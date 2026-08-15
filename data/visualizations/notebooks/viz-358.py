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

        Trend lines 1960-2024 for 8 countries spanning the full spectrum of aging.
        Japan's near-vertical climb illustrates the extreme case driven by longevity gains
        and falling fertility. South Korea is now on a similar trajectory. Brazil, China,
        and India are accelerating from low bases, with China's one-child legacy
        compressing what took Europe a century into just 30 years.
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
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = round(row["value"], 1)

    select = ["Japan", "Korea, Rep.", "Germany", "Italy", "France", "Brazil", "China", "India"]
    result = []
    for c in select:
        if c not in by_country:
            print(f"Missing: {c}")
            continue
        yv = by_country[c]
        pts = [{"y": y, "v": yv[y]} for y in range(1960, 2025, 2) if y in yv]
        name = "South Korea" if c == "Korea, Rep." else c
        result.append({"n": name, "pts": pts})
        print(f"{name}: {pts[0]['v']} -> {pts[-1]['v']}")
    return result, by_country, select


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with endpoint labels and resolveCollisions
        - **Countries**: Japan and South Korea (fastest aging), Germany/Italy/France (established
          European aging), Brazil/China/India (accelerating from low bases)
        - **Reference band**: 20% threshold (policy-significant aging level)
        - **Highlights**: Japan crosses 50% in 2022 — more elderly than working-age adults
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
