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
        # Youth Literacy Rate -- Methodology

        Horizontal bar chart showing youth literacy rates (ages 15-24)
        across ~56 individual countries, sorted from lowest to highest.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-ADT-1524-LT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SKIP_KW = ["income","OECD","World","IDA","IBRD","dividend","region","Pacific","Asia","Africa","Europe","America","Caribbean","Union","Euro area","Arab","states","Fragile","Least developed","South Asia","Sub-Saharan","Central Europe","Latin America","Heavily"]
    def is_country(name):
        for kw in SKIP_KW:
            if kw.lower() in name.lower():
                return False
        return True

    countries = [x for x in data if x["value"] is not None and x["country"] and len(x["country"]) == 2 and is_country(x["countryName"])]
    latest = {}
    for x in countries:
        if x["countryName"] not in latest or x["year"] > latest[x["countryName"]]["year"]:
            latest[x["countryName"]] = x
    filtered = sorted(latest.values(), key=lambda x: x["value"])
    print(f"Countries: {len(filtered)}")
    return (filtered,)


@app.cell
def _(filtered, json):
    chart_data = [{"n": x["countryName"], "v": round(x["value"], 1), "y": x["year"]} for x in filtered]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
