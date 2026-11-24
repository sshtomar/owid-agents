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
        # Tariff Rates on Manufactured Products — Methodology

        Documents the data pipeline behind viz-515: trend lines showing weighted mean tariff rates on manufactured goods.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--TM-TAX-MANF-WM-FN-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta_info = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta_info['title']}")
    return data, meta_info, raw


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
    print(f"Value range: {min(values):.2f} - {max(values):.2f}")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines chosen for time-series comparison across countries
        - **Country selection**: Selected to show range from high to low values and interesting trajectories
        - **Time range**: Full available range retained for maximum context
        """
    )
    return


@app.cell
def _(json, filtered):
    chart_data = [
        {"n": d["countryName"], "y": d["year"], "v": round(d["value"], 2)}
        for d in filtered
    ]
    print(json.dumps(chart_data[:5], separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
