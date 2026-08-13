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
        # Electricity from Hydropower, Top Countries -- Methodology

        Horizontal bar chart of the top 20 countries by share of electricity generated
        from hydroelectric sources (latest available year, 2021–2024).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-HYRO-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_country = {}
    for row in data:
        if row['value'] is not None and len(row['country']) == 2:
            n = row['countryName']
            if n not in by_country:
                by_country[n] = {}
            by_country[n][row['year']] = round(row['value'], 1)

    latest = {}
    for name, years in by_country.items():
        if years:
            yr = max(years.keys())
            if yr >= 2018:
                latest[name] = {"v": years[yr], "y": yr}

    by_val = sorted(latest.items(), key=lambda x: x[1]['v'], reverse=True)
    top20 = [{"n": name, "v": info["v"], "y": info["y"]} for name, info in by_val[:20]]

    for d in top20:
        print(f"  {d['n']} ({d['y']}): {d['v']:.1f}%")
    return top20, latest, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart ranked by % hydropower
        - **Country selection**: Top 20 by latest value (2018+), excluding regional aggregates
        - **Color encoding**: Deep green for near-100%; lighter shades as % falls
        - **Story**: Bhutan and Paraguay are effectively 100% hydro. Twelve countries get more
          than 60% from rivers — mostly in Africa and Latin America where major river systems
          provide abundant generation potential. Iceland's hydro is partly displaced by geothermal.
          Norway (88.6%) serves as a European benchmark.
        """
    )
    return


@app.cell
def _(json, top20):
    short = {"Central African Republic": "Cent. African Rep.", "Korea, Dem. People's Rep.": "N. Korea"}
    out = [{"n": short.get(d["n"], d["n"]), "v": d["v"], "y": d["y"]} for d in top20]
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
