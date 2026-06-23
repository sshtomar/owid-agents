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
        # Energy Use Per Capita, 1990 vs 2023 -- Methodology

        Slope chart comparing energy consumption per capita (kg of oil equivalent)
        at two points in time. Shows the enormous gap between rich and poor nations
        and changing trajectories.
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
    for row in data:
        if row["value"] is not None:
            by_country[row["countryName"]][row["year"]] = row["value"]

    selected = ["Canada", "Australia", "France", "Japan", "Germany",
                "China", "Brazil", "Indonesia", "India", "Ethiopia", "Bangladesh"]

    result = []
    for country in selected:
        if country in by_country:
            vals = by_country[country]
            a = vals.get(1990)
            b = None
            for yr in [2023, 2022, 2021]:
                if vals.get(yr) is not None:
                    b = vals[yr]
                    break
            if a and b:
                result.append({"n": country, "a": round(a, 0), "b": round(b, 0)})

    result.sort(key=lambda x: x["b"], reverse=True)
    for r in result:
        print(f"{r['n']}: {r['a']} -> {r['b']} ({r['b']-r['a']:+.0f})")
    return by_country, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- two-point comparison shows change at a glance
        - **Year selection**: 1990 vs 2023 (33-year span of globalization and energy transition)
        - **Key stories**:
          - Canada/Australia: highest consumers, barely changed (efficiency vs scale)
          - Germany/France/Japan: declining (efficiency gains)
          - China: tripled, now approaching European levels
          - India/Indonesia: growing but still far below
          - Ethiopia/Bangladesh: minimal energy use, slight growth
        - **Color**: by direction of change -- warm for risers, cool for decliners
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
