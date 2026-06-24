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
        # Net Forest Depletion (% of GNI) -- Methodology

        Trend lines showing how much national income is being lost through forest
        depletion for the 10 most affected countries, 2000-2021. Countries where
        average forest depletion exceeds 0.8% of GNI over 2010-2021 are included.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-ADJ-DFOR-GN-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    return data, raw


@app.cell
def _(json, data):
    AGGREGATES = {'Arab World','East Asia & Pacific','Euro area','Europe & Central Asia','World','High income','Low income','Middle income','Latin America & Caribbean','Sub-Saharan Africa','Africa Eastern and Southern','Africa Western and Central','Low & middle income','OECD members','Least developed countries: UN classification'}

    country_ts = {}
    for x in data:
        n = x['countryName']
        if n not in AGGREGATES and '(' not in n and 'excluding' not in n and x['value'] is not None:
            if n not in country_ts:
                country_ts[n] = {}
            country_ts[n][x['year']] = x['value']

    high = []
    for c, ts in country_ts.items():
        recent_vals = [ts[y] for y in range(2010, 2022) if y in ts]
        if recent_vals and sum(recent_vals)/len(recent_vals) > 0.8:
            high.append((c, sum(recent_vals)/len(recent_vals)))
    high.sort(key=lambda x: -x[1])
    top10 = [c for c,_ in high[:10]]

    chart_data = []
    for n in top10:
        ts = country_ts[n]
        pts = [{"y": y, "v": round(ts[y], 2)} for y in range(2000, 2022) if y in ts]
        if pts:
            chart_data.append({"n": n, "pts": pts})

    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, country_ts, high, top10


if __name__ == "__main__":
    app.run()
