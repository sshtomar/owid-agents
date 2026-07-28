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
        # Progress on Universal Health Coverage, 2000-2023 -- Methodology

        Slope chart showing UHC Service Coverage Index (SDG 3.8.1) from ~2000
        to ~2022 for 19 countries spread across the income spectrum. The index
        (0-100) measures coverage of essential health services.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--UHC_INDEX_REPORTED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso3_map = {
        'NOR':'Norway','CUB':'Cuba','NLD':'Netherlands','CHN':'China',
        'ARG':'Argentina','UKR':'Ukraine','PRY':'Paraguay','JAM':'Jamaica',
        'BTN':'Bhutan','PHL':'Philippines','SWZ':'Eswatini','PAK':'Pakistan',
        'COM':'Comoros','BDI':'Burundi','ERI':'Eritrea','NER':'Niger',
        'BEN':'Benin','MDG':'Madagascar','ETH':'Ethiopia'
    }

    by_country = {}
    for p in data:
        c = p["country"]
        if c not in iso3_map:
            continue
        if c not in by_country:
            by_country[c] = []
        by_country[c].append((p["year"], p["value"]))

    slope = []
    for code, name in iso3_map.items():
        pts = sorted(by_country.get(code, []))
        early = [(y, v) for y, v in pts if 2000 <= y <= 2002]
        late = [(y, v) for y, v in pts if 2020 <= y <= 2023]
        if early and late:
            a, b = early[-1][1], late[-1][1]
            slope.append({"n": name, "a": a, "b": b})
            print(f"  {name}: {a} -> {b} (+{b-a})")

    slope.sort(key=lambda x: -x["b"])
    return slope, by_country, iso3_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (~2000 vs ~2022) to show progress magnitude
        - **Color**: Green diverging ramp (dark green = biggest gains)
        - **Story**: China improved from 65 to 85, nearly matching Norway (89).
          Ethiopia rose from 14 to 33 — a 136% increase but still among the lowest globally.
          All 19 countries improved; no country regressed over this period.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
