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
        # Employment in Industry: 1995 vs. 2022 — Methodology

        Slope chart comparing the share of employment in industry (manufacturing,
        construction, mining) between 1995 and 2022. Shows deindustrialization in
        rich economies alongside industrialization in South and East Asia.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-IND-EMPL-ZS.json"
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

    targets = [
        "Czechia","Bulgaria","Germany","Korea, Rep.","Italy","Japan",
        "Ireland","Hong Kong SAR, China","France","Greece",
        "China","Indonesia","India","Bangladesh","Ethiopia"
    ]
    name_map = {
        "Korea, Rep.": "Korea",
        "Hong Kong SAR, China": "Hong Kong"
    }
    slope = []
    for country in targets:
        if country not in by_country:
            print(f"MISSING: {country}")
            continue
        y95 = by_country[country].get(1995)
        y22 = by_country[country].get(2022)
        if y95 is None or y22 is None:
            print(f"NO DATA: {country}")
            continue
        name_short = name_map.get(country, country)
        change = round(y22 - y95, 1)
        print(f"{name_short}: {round(y95,1)}% -> {round(y22,1)}% ({change:+.1f}pp)")
        slope.append({"n": name_short, "a": round(y95, 1), "b": round(y22, 1)})

    slope.sort(key=lambda x: -x["a"])
    return by_country, slope, targets


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparison across many entities
        - **Country selection**: 15 countries chosen to show both ends of the story:
          deindustrializing rich economies and industrializing Asia
        - **Years**: 1995 vs 2022 (broadest common coverage in ILO-modelled estimates)
        - **Color encoding**: Warm (red/orange) = shrinking share; Green = growing share
        - **Key insights**:
          - Hong Kong: steepest absolute decline, from 27% to 14% (finance replaced industry)
          - India: largest absolute gain, from 15% to 26% (manufacturing growth)
          - China also grew (23% to 31%) while already-industrialized neighbors declined
          - Ethiopia: barely changed (6.5% to 6.3%) — still pre-industrial
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
