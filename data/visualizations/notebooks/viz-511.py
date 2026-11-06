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
        # Births by Caesarean Section -- Methodology

        Shows the global spectrum of c-section rates, from over-medicalization
        to critically low access. WHO optimal range is 10-15%.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHS4_115.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    filtered.sort(key=lambda x: x["value"], reverse=True)
    print(f"After filtering: {len(filtered)} rows")
    values = [d["value"] for d in filtered]
    print(f"Range: {min(values):.1f} - {max(values):.1f}")
    return (filtered,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart -- best for ranked cross-country comparison
        - **Country selection**: Top 20 (over-medicalized) and bottom 20 (under-serviced)
        - **WHO reference band**: 10-15% optimal range shown as a vertical band
        - **Color**: Warm (red/orange) for high rates, cool (gray) for critically low
        - **Story**: Dominican Republic at 58% vs Chad at 1.4% -- a 40x gap in access
        """
    )
    return


@app.cell
def _(json, filtered):
    names = {
        "DOM": "Dominican Rep.", "CYP": "Cyprus", "BRA": "Brazil", "EGY": "Egypt",
        "CHL": "Chile", "ECU": "Ecuador", "TUR": "Turkey", "LBN": "Lebanon",
        "PRY": "Paraguay", "COL": "Colombia", "IRN": "Iran", "MUS": "Mauritius",
        "GEO": "Georgia", "MDV": "Maldives", "MEX": "Mexico", "CUB": "Cuba",
        "ROU": "Romania", "URY": "Uruguay", "BGR": "Bulgaria", "KOR": "South Korea",
        "MOZ": "Mozambique", "LBR": "Liberia", "GNB": "Guinea-Bissau", "LAO": "Laos",
        "BFA": "Burkina Faso", "AGO": "Angola", "CIV": "Ivory Coast", "GIN": "Guinea",
        "SLE": "Sierra Leone", "ERI": "Eritrea", "NGA": "Nigeria", "AFG": "Afghanistan",
        "CMR": "Cameroon", "GMB": "Gambia", "MLI": "Mali", "MDG": "Madagascar",
        "ETH": "Ethiopia", "TLS": "Timor-Leste", "NER": "Niger", "TCD": "Chad"
    }
    top20 = [{"n": names.get(d["country"], d["country"]), "v": round(d["value"], 1)} for d in filtered[:20]]
    bot20 = [{"n": names.get(d["country"], d["country"]), "v": round(d["value"], 1)} for d in filtered[-20:]]
    chart_data = top20 + bot20
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
