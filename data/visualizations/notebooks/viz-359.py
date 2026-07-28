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
        # Hydropower Dependency: Countries Near 100% -- Methodology

        Trend lines showing the share of electricity production from hydroelectric
        sources (1990-2024) for countries that rely almost entirely on water.
        Highlights climate vulnerability: drought can cut national power supply.
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
    skip_kw = ['income','World','Asia','Africa','America','Europe','Pacific','Atlantic',
               'Caribbean','Central','Middle','Sub-Saharan','dividend','Arab','IBRD',
               'IDA','OECD','small states','Early','Late','Low','High','Upper','Lower',
               'Fragile','East','South','North','Least','Heavily','Euro']

    country_data = [p for p in data if p["value"] is not None
                    and not any(k in p["countryName"] for k in skip_kw)]

    by_country = {}
    for p in country_data:
        c = p["countryName"]
        if c not in by_country:
            by_country[c] = []
        by_country[c].append((p["year"], p["value"]))

    selected = ['Congo, Dem. Rep.','Albania','Ethiopia','Cameroon',
                'Georgia','Ecuador','Costa Rica','Angola','Iceland']

    chart_data = []
    for c in selected:
        if c in by_country:
            pts = sorted(by_country[c])
            sampled = [(y, round(v, 1)) for y, v in pts if y % 2 == 0 or y == pts[-1][0]]
            chart_data.append({"n": c, "pts": [{"y": y, "v": v} for y, v in sampled]})
            avg = sum(v for y, v in pts) / len(pts)
            print(f"  {c}: avg={avg:.0f}%, n_pts={len(pts)}, range={pts[0][0]}-{pts[-1][0]}")
    return chart_data, by_country, selected, country_data, skip_kw


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines with endpoint labels and collision resolution
        - **Color**: 9 distinct editorial palette colors
        - **Story**: Congo DRC and Albania are virtually 100% hydro throughout.
          Cameroon dropped sharply from 99% to ~63% as the economy diversified.
          Ecuador fluctuated widely based on rainfall variability.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
