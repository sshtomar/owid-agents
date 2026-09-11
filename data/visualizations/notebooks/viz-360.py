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
    mo.md("# Depression Prevalence Bar Chart — Methodology\n\nHorizontal bar chart ranking countries by estimated depression prevalence (2015). Data from WHO GHO indicator GDO_q35. ISO3 country codes are mapped to display names.")
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--GDO_q35.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points (single year 2015, ISO3 country codes)")
    return data, raw


@app.cell
def _(data, json):
    iso3_names = {
        "UKR": "Ukraine", "AUS": "Australia", "EST": "Estonia", "USA": "USA",
        "BRA": "Brazil", "GRC": "Greece", "PRT": "Portugal", "LTU": "Lithuania",
        "FIN": "Finland", "BLR": "Belarus", "RUS": "Russia", "CUB": "Cuba",
        "MDA": "Moldova", "NZL": "New Zealand", "BRB": "Barbados", "PRY": "Paraguay",
        "ESP": "Spain", "DEU": "Germany", "BHS": "Bahamas", "TTO": "Trinidad & Tobago",
        "CZE": "Czechia", "BGR": "Bulgaria", "ITA": "Italy", "ARE": "UAE",
        "HUN": "Hungary", "SVN": "Slovenia", "SVK": "Slovakia", "AUT": "Austria",
        "HRV": "Croatia", "MLT": "Malta", "NPL": "Nepal", "LAO": "Laos",
        "KIR": "Kiribati", "VUT": "Vanuatu", "TLS": "Timor-Leste", "PNG": "Papua N. Guinea",
        "SLB": "Solomon Is.",
    }
    filtered = [d for d in data if d["value"] is not None]
    sorted_data = sorted(filtered, key=lambda x: x["value"], reverse=True)
    chart_data = [{"n": iso3_names.get(d["country"], d["country"]), "v": round(d["value"], 2)}
                  for d in sorted_data[:30] + sorted_data[-7:]]
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
