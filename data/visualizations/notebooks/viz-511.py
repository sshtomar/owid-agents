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
        # Prenatal Care Coverage -- Methodology

        This notebook documents the data pipeline and editorial decisions
        behind the slope chart showing change in prenatal care coverage
        between the early 2000s and late 2010s.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-ANVC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SKIP = [
        'IDA','IBRD','income','Sub-','Africa','Asia','Europe','Pacific','America',
        'World','dividend','blend','Euro area','OECD','Arab World','Middle East',
        'Caribbean','Fragility','Conflict','Violence','Least developed','Heavily',
        'HIPC','South Asia','countries:'
    ]
    def is_country(row):
        name = row["countryName"]
        return not any(kw in name for kw in SKIP)

    def normalize_name(name):
        replacements = {
            "Egypt, Arab Rep.": "Egypt",
            "Congo, Dem. Rep.": "DR Congo",
            "Congo, Rep.": "Congo",
            "Cote d'Ivoire": "Cote d'Ivoire",
            "Cabo Verde": "Cabo Verde",
            "Gambia, The": "Gambia",
        }
        return replacements.get(name, name)

    country_data = [r for r in data if is_country(r)]
    country_records = {}
    for r in country_data:
        c = r["countryName"]
        if c not in country_records:
            country_records[c] = []
        country_records[c].append(r)
    for c in country_records:
        country_records[c].sort(key=lambda x: x["year"])
    print(f"Country-level records: {len(country_records)} countries")
    return country_records, country_data, is_country, normalize_name


@app.cell
def _(country_records, normalize_name):
    early_window = (2000, 2010)
    recent_window = (2013, 2021)

    slope_data = []
    for country, records in country_records.items():
        early = [r for r in records if early_window[0] <= r["year"] <= early_window[1]]
        recent = [r for r in records if recent_window[0] <= r["year"] <= recent_window[1]]
        if early and recent:
            a_rec = early[-1]
            b_rec = recent[-1]
            slope_data.append({
                "n": normalize_name(country),
                "a": round(a_rec["value"], 1),
                "b": round(b_rec["value"], 1),
                "ay": a_rec["year"],
                "by": b_rec["year"],
            })

    slope_data.sort(key=lambda x: x["a"])
    print(f"Countries with data in both windows: {len(slope_data)}")
    for s in slope_data[:5]:
        print(f"  {s}")
    return (slope_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart comparing early 2000s to late 2010s coverage
        - **Country selection**: 20 countries spanning the full range (27%-100%)
          including outliers like Ethiopia (huge gain), Burkina Faso (large decline)
        - **Color encoding**: By change magnitude — green=large gain, amber=small change, red=decline
        - **Story**: Most low-coverage countries improved, but a few declined;
          Chad and Afghanistan remain persistently low
        """
    )
    return


@app.cell
def _(json, slope_data):
    SELECTED = [
        'Ethiopia','Bangladesh','Chad','Afghanistan',
        'Egypt','India','Angola','Haiti',
        "Cote d'Ivoire",'Bolivia','Kenya',
        'Cambodia','Algeria','China',
        'Burkina Faso','Colombia','Albania',
        'Brazil','Argentina','Cuba'
    ]
    chart_data = [
        {"n": s["n"], "a": s["a"], "b": s["b"]}
        for s in slope_data
        if s["n"] in SELECTED
    ]
    chart_data.sort(key=lambda x: x["a"])
    print(f"Final chart data: {len(chart_data)} countries")
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
