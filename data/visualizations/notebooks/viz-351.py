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
        # Adult Mortality Rate — Methodology

        Slope chart comparing adult mortality (~2000 vs ~2019) across 26 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHOSIS_000004.json"
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
    countries = sorted(set(d["country"] for d in filtered))
    years = sorted(set(d["year"] for d in filtered))
    print(f"Country codes: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.1f} - {max(values):.1f}")
    return countries, values, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point (near-2000 vs near-2019) shows who improved most
        - **Data note**: WHO data is sparse; nearest year within ±3 of target used per country
        - **Country selection**: 26 countries with data near both endpoints, mapped from ISO3 codes
        - **Color**: By percentage change — teal for >50% decline, steel blue for 25-50%, green for 0-25%, red for increase
        - **Highlight**: Uzbekistan -65%; France, Greece, Switzerland all cut by ~50%+
        """
    )
    return


@app.cell
def _(json, filtered):
    iso3_map = {
        "BWA": "Botswana", "KWT": "Kuwait", "RUS": "Russia", "ISL": "Iceland",
        "PRT": "Portugal", "MUS": "Mauritius", "TUN": "Tunisia", "ARE": "UAE",
        "AFG": "Afghanistan", "GBR": "UK", "BRB": "Barbados", "LTU": "Lithuania",
        "CHN": "China", "ESP": "Spain", "HRV": "Croatia", "MAR": "Morocco",
        "IND": "India", "BRA": "Brazil", "USA": "USA", "FRA": "France",
        "DEU": "Germany", "JPN": "Japan", "MEX": "Mexico", "NGA": "Nigeria",
        "ETH": "Ethiopia", "BGD": "Bangladesh", "ZAF": "South Africa",
        "IDN": "Indonesia", "PAK": "Pakistan", "TUR": "Turkey", "IRN": "Iran",
        "KEN": "Kenya", "TZA": "Tanzania", "GHA": "Ghana", "EGY": "Egypt",
        "SAU": "Saudi Arabia", "ARG": "Argentina", "COL": "Colombia",
        "PHL": "Philippines", "VNM": "Vietnam", "THA": "Thailand",
        "KOR": "South Korea", "AUT": "Austria", "CHE": "Switzerland",
        "BEL": "Belgium", "NOR": "Norway", "SWE": "Sweden", "ITA": "Italy",
        "ZWE": "Zimbabwe", "SEN": "Senegal", "HTI": "Haiti", "BOL": "Bolivia",
        "PER": "Peru", "CHL": "Chile", "CUB": "Cuba", "DOM": "Dominican Rep.",
        "MYS": "Malaysia", "SGP": "Singapore", "UZB": "Uzbekistan",
        "HUN": "Hungary", "GRC": "Greece",
    }

    by_code = {}
    for r in filtered:
        by_code.setdefault(r["country"], {})[r["year"]] = r["value"]

    def get_nearest(pts, target, window=3):
        for dy in range(window + 1):
            for y in [target + dy, target - dy]:
                if y in pts:
                    return pts[y]
        return None

    chart_data = []
    for code, pts in by_code.items():
        if code not in iso3_map:
            continue
        a = get_nearest(pts, 2000)
        b = get_nearest(pts, 2019)
        if a is None or b is None:
            continue
        chart_data.append({"n": iso3_map[code], "a": round(a, 1), "b": round(b, 1)})

    chart_data.sort(key=lambda x: -x["a"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
