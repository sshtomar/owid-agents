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
        # HDL Cholesterol by Country — Methodology

        Horizontal bar chart of mean age-standardized HDL cholesterol (mmol/L)
        for 30 countries in 2018 (viz-516).

        HDL ("good") cholesterol is inversely associated with cardiovascular risk.
        Values below 1.0 mmol/L are considered low.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_CHOL_MEANHDL_A.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points, year range: {raw['meta']['dateRange']}")
    return data, raw


@app.cell
def _(json, data):
    iso_map = {
        "AND": "Andorra", "AUS": "Australia", "BHR": "Bahrain",
        "BLR": "Belarus", "BRB": "Barbados", "BRN": "Brunei",
        "CHN": "China", "COD": "DR Congo", "COG": "Congo",
        "CZE": "Czechia", "DJI": "Djibouti", "DOM": "Dom. Republic",
        "DNK": "Denmark", "EGY": "Egypt", "GIN": "Guinea",
        "GTM": "Guatemala", "HTI": "Haiti", "IRN": "Iran",
        "KEN": "Kenya", "MHL": "Marshall Islands", "MLT": "Malta",
        "MWI": "Malawi", "MYS": "Malaysia", "NGA": "Nigeria",
        "NLD": "Netherlands", "NOR": "Norway", "PRK": "North Korea",
        "SDN": "Sudan", "CHE": "Switzerland", "URY": "Uruguay",
        "UZB": "Uzbekistan",
    }

    data_2018 = [
        {"n": iso_map.get(pt["country"], pt["country"]), "v": round(pt["value"], 1)}
        for pt in data
        if pt["year"] == 2018 and pt["value"] is not None
        and pt["country"] not in ("AFR", "AMR", "EMR", "EUR", "SEAR", "WPR")
    ]
    data_2018.sort(key=lambda x: -x["v"])

    print(f"2018 data: {len(data_2018)} countries")
    for row in data_2018:
        print(f"  {row['n']}: {row['v']}")
    print(json.dumps(data_2018, separators=(",", ":")))
    return (data_2018,)


if __name__ == "__main__":
    app.run()
