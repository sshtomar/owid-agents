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
        # Age Dependency Ratio -- Methodology

        Slope chart comparing 1970 vs 2022 age dependency ratio for diverse countries.
        Shows Sub-Saharan Africa still high, Asia dramatically reduced, Japan reversed.
        Source: World Bank SP.POP.DPND
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    exclude_kw = ["World","income","OECD","Euro","IDA","IBRD","dividend","poor","states",
                  "excluding","Blend","Arab","Africa","Asia","Latin","North America",
                  "Pacific","Caribbean","Central","Eastern","Western","Southern","Northern",
                  "Middle","Least","Sub-Saharan","classification","&"]
    def is_country(name): return not any(kw.lower() in name.lower() for kw in exclude_kw)

    yr1970 = {p["countryName"]: round(p["value"], 1) for p in data if p["year"] == 1970 and p["value"] is not None and is_country(p["countryName"])}
    yr2022 = {p["countryName"]: round(p["value"], 1) for p in data if p["year"] == 2022 and p["value"] is not None and is_country(p["countryName"])}

    selected = [
        "Chad", "Angola", "Burkina Faso", "Congo, Dem. Rep.",
        "Ethiopia", "Kenya", "Ghana",
        "India", "Bangladesh",
        "China", "Korea, Rep.", "Japan",
        "Brazil", "Colombia", "Iran, Islamic Rep.",
        "Germany", "France", "Italy"
    ]
    chart_data = []
    for n in selected:
        if n in yr1970 and n in yr2022:
            chart_data.append({"n": n, "a": yr1970[n], "b": yr2022[n]})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, selected, yr1970, yr2022


if __name__ == "__main__":
    app.run()
