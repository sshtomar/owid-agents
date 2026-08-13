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
        # Terrestrial and Marine Protected Areas, 2024 -- Methodology

        Horizontal bar chart of the top 20 countries by share of territory (land + sea)
        under formal protection. Bhutan leads at over 50%; most countries fall below 30%.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-PTD-TOTL-ZS.json"
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
            if yr >= 2020:
                latest[name] = {"v": years[yr], "y": yr}

    by_val = sorted(latest.items(), key=lambda x: x[1]['v'], reverse=True)
    top20 = [{"n": name, "v": info["v"], "y": info["y"]} for name, info in by_val[:20]]

    for d in top20:
        print(f"  {d['n']} ({d['y']}): {d['v']:.1f}%")
    return top20, latest, by_country, by_val


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — easy to compare ranked absolute values
        - **Country selection**: Top 20 by most recent value (2020+), excluding regional aggregates
        - **Color encoding**: Graduated green from light (20-30%) to deep (40%+)
        - **Story**: Wide variation — Bhutan at 51.6% reflects Buddhist conservation philosophy;
          Germany at 40% reflects EU Natura 2000 network; Congo Rep. at 33% has large intact
          rainforest under protection. The global 30x30 target (30% by 2030) is within reach
          for some, but most nations are well below it.
        """
    )
    return


@app.cell
def _(json, top20):
    print(json.dumps(top20, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
