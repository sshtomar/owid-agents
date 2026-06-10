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
        # Neonatal Mortality Rate — Methodology

        Six decades of progress in neonatal survival across diverse countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-NMRT.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None and 1960 <= d["year"] <= 2024]
    print(f"After filtering: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f}")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows decline trajectory over 60 years for 9 countries
        - **Country selection**: Diverse income levels and regions; Bangladesh included for dramatic fall from 103 to 18
        - **Time range**: 1960–2024 where available per country
        - **Highlights**: China fell 90% from 30 to 3; Japan reached 0.9; Sub-Saharan Africa (Kenya) stalled 1990–2010
        """
    )
    return


@app.cell
def _(json, filtered):
    SELECTED = ["Bangladesh", "India", "Ethiopia", "Kenya", "Indonesia",
                "Brazil", "China", "Germany", "Japan"]
    countries_map = {}
    for r in filtered:
        countries_map.setdefault(r["countryName"], {})[r["year"]] = r["value"]

    chart_data = []
    for name in SELECTED:
        if name not in countries_map:
            continue
        pts = sorted(countries_map[name].items())
        pts_thinned = [(y, v) for y, v in pts if y % 5 == 0 or y == max(countries_map[name])]
        chart_data.append({
            "n": name,
            "pts": [{"y": y, "v": round(v, 2)} for y, v in pts_thinned]
        })

    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
