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
        # Out-of-Pocket Health Expenditure -- Methodology

        Horizontal bar chart showing share of health spending paid directly
        by patients, from highest (Armenia ~80%) to lowest (France ~9%).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-OOPC-CH-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    SKIP_KW = ["income","OECD","World","IDA","IBRD","dividend","region","Pacific","Asia","Africa","Europe","America","Caribbean","Union","Euro area","Arab","states","Fragile","South Asia","Sub-Saharan","Heavily","North Africa","Middle East"]
    def is_ok(name):
        for kw in SKIP_KW:
            if kw.lower() in name.lower():
                return False
        return True
    countries = [x for x in data if x["value"] is not None and x["country"] and len(x["country"]) == 2 and is_ok(x["countryName"])]
    latest = {}
    for x in countries:
        if x["countryName"] not in latest or x["year"] > latest[x["countryName"]]["year"]:
            latest[x["countryName"]] = x
    result = sorted([v for v in latest.values() if v["year"] >= 2017], key=lambda x: x["value"], reverse=True)
    chart_data = [{"n": x["countryName"], "v": round(x["value"], 1), "y": x["year"]} for x in result]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
