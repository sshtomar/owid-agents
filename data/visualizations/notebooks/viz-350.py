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
        # Energy Use per Capita — Methodology

        Slope chart comparing 1990 vs 2020 energy consumption across 19 countries.
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
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    values = [d["value"] for d in filtered]
    countries = sorted(set(d["countryName"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.0f} - {max(values):.0f} kg/cap")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point comparison 1990 vs 2020 shows direction and magnitude
        - **Country selection**: 19 countries spanning ultra-high (Iceland 16k) to low (Bangladesh 279)
        - **Color**: By percentage change — large increases in orange-red, declines in green
        - **Highlight**: South Korea +149%, Iran +174%; Western Europe mostly declining
        """
    )
    return


@app.cell
def _(json, filtered):
    countries_map = {}
    for r in filtered:
        countries_map.setdefault(r["countryName"], {})[r["year"]] = r["value"]

    SELECTED = {
        "Iceland": "Iceland", "Bahrain": "Bahrain", "Brunei Darussalam": "Brunei",
        "Canada": "Canada", "Finland": "Finland", "Australia": "Australia",
        "Belgium": "Belgium", "Germany": "Germany", "France": "France",
        "Japan": "Japan", "Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran",
        "Brazil": "Brazil", "China": "China", "Kenya": "Kenya",
        "Indonesia": "Indonesia", "Ethiopia": "Ethiopia", "India": "India",
        "Bangladesh": "Bangladesh"
    }

    def get_nearest(pts, target, window=3):
        for dy in range(window + 1):
            for y in [target + dy, target - dy]:
                if y in pts:
                    return pts[y]
        return None

    chart_data = []
    for name, display in SELECTED.items():
        if name not in countries_map:
            continue
        pts = countries_map[name]
        a = get_nearest(pts, 1990)
        b = get_nearest(pts, 2020)
        if a is None or b is None:
            continue
        chart_data.append({"n": display, "a": round(a), "b": round(b)})

    chart_data.sort(key=lambda x: -x["a"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
