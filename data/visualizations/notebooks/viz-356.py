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
        # Renewable Energy Share of Total Consumption, 1990 vs 2021 -- Methodology

        Slope chart comparing the share of renewables in total final energy consumption
        between 1990 and 2021. Reveals the paradox: poor countries have always had
        "high renewables" from traditional biomass burning, while rich countries
        are just beginning the transition to modern clean energy.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-FEC-RNEW-ZS.json"
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
            by_country[row["countryName"]][row["year"]] = row["value"]

    selected = [
        "Congo, Dem. Rep.", "Ethiopia", "Iceland", "Finland", "Brazil",
        "Denmark", "India", "Canada", "Indonesia", "Germany", "France",
        "China", "Australia", "Japan"
    ]

    result = []
    for c in selected:
        if c in by_country:
            vals = by_country[c]
            a = vals.get(1990)
            b = vals.get(2021) or vals.get(2020) or vals.get(2019)
            if a is not None and b is not None:
                result.append({"n": c, "a": round(a, 1), "b": round(b, 1)})

    result.sort(key=lambda x: x["b"], reverse=True)
    for r in result:
        print(f"{r['n']}: {r['a']}% -> {r['b']}% ({r['b']-r['a']:+.1f})")
    return by_country, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- compares two time points, shows direction of change
        - **Year selection**: 1990 vs 2021 (latest complete year)
        - **Key stories**:
          - Congo/Ethiopia: near-100% renewables but from traditional wood burning, slowly declining
          - Iceland: high geothermal/hydro, rising to 82%
          - Denmark: massive modern energy transition (+32pp)
          - Germany: from near-zero to 18% (+16pp) via solar/wind policy
          - India/Indonesia/China: declining as they build fossil fuel capacity faster
          - Note: traditional biomass inflates developing-country numbers
        - **Color**: warm (rising) vs cool (falling)
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
