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
        # Electric Power Grid Losses (1990 vs 2020) -- Methodology

        Slope chart showing electric power transmission and distribution losses
        as a percentage of total output across 20 countries in 1990 and 2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-LOSS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    AGGREGATE_CODES = {
        "1A","Z4","4E","XC","Z7","7E","T4","XE","XD","XF","ZT","XH","XI","XG","V3","ZJ","XJ","T2",
        "XL","XO","XM","XN","ZQ","XQ","T3","XP","XU","OE","S4","S2","V4","V1","S1","8S","T5","ZG",
        "ZF","T6","XT","1W","ZH","ZI","F1","B8","V2","EU","T7","S3"
    }
    NAME_MAP = {
        "Iraq": "Iraq",
        "Congo, Rep.": "Congo (Rep.)",
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "S. Korea",
    }
    SELECTED = ["IQ","CG","HN","TD","JM","KE","CM","EG","ET","IN","AL","BD","BO","CO","FR","DE","JP","CN","KR","AU"]

    country_vals = {}
    for pt in data:
        code = pt["country"]
        if code in AGGREGATE_CODES:
            continue
        if code not in SELECTED:
            continue
        cn = pt["countryName"]
        yr = pt["year"]
        v = pt["value"]
        if v is not None:
            if code not in country_vals:
                country_vals[code] = {"name": NAME_MAP.get(cn, cn), "values": {}}
            country_vals[code]["values"][yr] = v

    chart_data = []
    for code, info in country_vals.items():
        if 1990 in info["values"] and 2020 in info["values"]:
            chart_data.append({"n": info["name"], "a": round(info["values"][1990], 1), "b": round(info["values"][2020], 1)})
    chart_data.sort(key=lambda x: x["b"], reverse=True)
    print(json.dumps(chart_data, separators=(",", ":")))
    return AGGREGATE_CODES, NAME_MAP, SELECTED, chart_data, code, country_vals, info


if __name__ == "__main__":
    app.run()
