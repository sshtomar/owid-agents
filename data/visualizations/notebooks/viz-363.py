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
        # Fossil Fuel Energy Consumption -- Methodology

        Documents the data behind viz-363: slope chart comparing 1995 vs 2015
        fossil fuel % of total energy consumption for 15 countries.
        Source: World Bank EG.USE.COMM.FO.ZS
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-COMM-FO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    # Selected countries for slope chart: 1995 vs 2015
    # Story: Japan increased (Fukushima shutdown), Brazil/Iceland/Denmark dramatically reduced
    yr1995 = {p["countryName"]: round(p["value"], 1) for p in data if p["year"] == 1995 and p["value"] and p["value"] > 0}
    yr2015 = {p["countryName"]: round(p["value"], 1) for p in data if p["year"] == 2015 and p["value"] and p["value"] > 0}

    selected_names = [
        "Japan", "Australia", "Korea, Rep.", "Germany", "China", "France",
        "Denmark", "Iceland", "Brazil", "India", "Indonesia", "Finland",
        "Austria", "Canada", "Italy"
    ]
    chart_data = []
    for n in selected_names:
        if n in yr1995 and n in yr2015:
            chart_data.append({"n": n, "a": yr1995[n], "b": yr2015[n]})

    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, selected_names, yr1995, yr2015


if __name__ == "__main__":
    app.run()
