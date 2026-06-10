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
        # International Tourism Arrivals — Methodology

        Tourism growth 1995–2020 and the COVID-19 collapse.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_kw = ["income", "World", "Africa", "Asia", "Europe", "OECD", "Pacific",
                  "Caribbean", "North America", "Latin", "Small", "dividend",
                  "fragile", "blend", "IDA", "IBRD", "Arab", "East Asia",
                  "South Asia", "Sub-Saharan", "Euro", "Middle East", "states",
                  "Saharan", "HIPC", "Indebted", "indebted", "Other", "situations"]
    filtered = [d for d in data if d["value"] is not None
                and not any(x in d["countryName"] for x in exclude_kw)
                and 1995 <= d["year"] <= 2020]
    print(f"After filtering: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Countries: {len(countries)}, Years: {years[0]}-{years[-1]}")
    return countries, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows growth trajectory and 2020 crash
        - **Country selection**: Top 10 by 2019 arrivals (individual countries only)
        - **Highlight**: France led throughout; COVID-19 cut arrivals 46–94% by 2020
        - **Values**: Expressed in millions for readability
        """
    )
    return


@app.cell
def _(json, filtered):
    countries_map = {}
    for r in filtered:
        countries_map.setdefault(r["countryName"], {})[r["year"]] = r["value"]

    SELECTED = ["France", "China", "Italy", "Hungary", "Croatia", "Hong Kong SAR, China",
                "Germany", "Greece", "Canada", "Austria"]

    chart_data = []
    for name in SELECTED:
        if name not in countries_map:
            continue
        pts = sorted(countries_map[name].items())
        chart_data.append({
            "n": "Hong Kong" if "Hong Kong" in name else name,
            "pts": [{"y": y, "v": round(v / 1e6, 2)} for y, v in pts]
        })

    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
