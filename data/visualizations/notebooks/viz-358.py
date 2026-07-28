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
        # Child Wasting: Most Affected Countries -- Methodology

        Horizontal bar chart of child wasting prevalence (% of children under 5
        with low weight-for-height) in the most recent survey year since 2015.
        Wasting is acute malnutrition and a major driver of child mortality.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-STA-WAST-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_kw = ['income','World','Asia','Africa','America','Europe','Pacific','Atlantic',
               'Caribbean','Central','Middle','Sub-Saharan','dividend','Arab','IBRD',
               'IDA','OECD','small states','Early','Late','Low','High','Upper','Lower',
               'Fragile','East','South','North','Least','Heavily']

    country_data = [p for p in data if p["value"] is not None
                    and not any(k in p["countryName"] for k in skip_kw)]

    latest = {}
    for p in country_data:
        c = p["countryName"]
        if c not in latest or p["year"] > latest[c][0]:
            latest[c] = (p["year"], p["value"])

    recent_high = {c: (y, v) for c, (y, v) in latest.items() if y >= 2015 and v >= 3.5}
    chart_data = sorted(
        [{"n": c, "v": round(v, 1), "y": y} for c, (y, v) in recent_high.items()],
        key=lambda x: -x["v"]
    )[:20]

    print(f"Countries with wasting >= 3.5% (2015+): {len(recent_high)}, showing top {len(chart_data)}")
    for d in chart_data:
        print(f"  {d['n']} ({d['y']}): {d['v']}%")
    return chart_data, latest, country_data, recent_high, skip_kw


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Ranked horizontal bar chart (clearest for country comparison)
        - **Color**: Warm ramp (red for severe, amber for moderate, green for lower)
        - **Story**: India's 18.7% wasting rate is dramatically above all other countries.
          South Asia and West Africa dominate the top 20. Global threshold for "high" wasting is 10%.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
