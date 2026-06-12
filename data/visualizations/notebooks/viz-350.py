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
        # Energy Use per Capita Divergence — Methodology

        Shows how primary energy use per person has evolved differently across
        the income spectrum: rich nations plateau, China triples, South Asia barely moves.
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
    target = {'Canada','Germany','Japan','Korea, Rep.','China','Brazil','India','Bangladesh'}
    filtered = [d for d in data if d['countryName'] in target and d['value'] is not None]
    countries = sorted(set(d['countryName'] for d in filtered))
    years = sorted(set(d['year'] for d in filtered))
    values = [d['value'] for d in filtered]
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.0f} - {max(values):.0f} kg oil equivalent/person")
    return countries, filtered, target, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — annual 1990-2020, 8 countries
        - **Country selection**: Canada (high+stable), Germany (high, declining), Japan (high, declining), Korea (rising rich), China (dramatic rise), Brazil (middle), India (low, growing), Bangladesh (very low)
        - **Highlight**: China's trajectory crosses all developing world countries and approaches Germany by 2020
        - **Story**: The energy transition challenge — rich nations can cut, but growing economies need more energy
        - **Note**: US not available in this dataset; Canada and "North America" aggregate available
        """
    )
    return


@app.cell
def _(json, filtered):
    chart_data = [
        {"n": d["countryName"], "y": d["year"], "v": round(d["value"])}
        for d in sorted(filtered, key=lambda x: (x["countryName"], x["year"]))
    ]
    print(json.dumps(chart_data[:5], separators=(",", ":")))
    print(f"... ({len(chart_data)} total rows)")
    return (chart_data,)


if __name__ == "__main__":
    app.run()
