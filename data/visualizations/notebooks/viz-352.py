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
        # Energy Use per Capita (1990 vs 2020) -- Methodology

        Slope chart comparing energy consumption per capita (kg of oil equivalent)
        across 18 countries between 1990 and 2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-USE-PCAP-KG-OE.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    AGGREGATE_CODES = {
        "1A","Z4","4E","XC","Z7","7E","T4","XE","XD","XF","ZT","XH","XI","XG","V3","ZJ","XJ","T2",
        "XL","XO","XM","XN","ZQ","XQ","T3","XP","XU","OE","S4","S2","V4","V1","S1","8S","T5","ZG",
        "ZF","T6","XT","1W","ZH","ZI","F1","B8","V2","EU","T7","S3"
    }
    country_vals = {}
    for pt in data:
        code = pt["country"]
        if code in AGGREGATE_CODES:
            continue
        cn = pt["countryName"]
        yr = pt["year"]
        v = pt["value"]
        if v is not None:
            if code not in country_vals:
                country_vals[code] = {"name": cn, "values": {}}
            country_vals[code]["values"][yr] = v

    with_both = {c: info for c, info in country_vals.items() if 1990 in info["values"] and 2020 in info["values"]}
    print(f"Countries with 1990 and 2020 data: {len(with_both)}")
    return AGGREGATE_CODES, country_vals, with_both


@app.cell
def _(json, with_both):
    NAME_MAP = {
        "Korea, Rep.": "S. Korea",
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
    }
    SELECTED = ["CA","FI","KR","AU","BE","CZ","DE","IR","FR","JP","HU","DK","CN","IT","CL","BR","EG","IN"]
    chart_data = []
    for code, info in with_both.items():
        if code not in SELECTED:
            continue
        name = NAME_MAP.get(info["name"], info["name"])
        a = round(info["values"][1990])
        b = round(info["values"][2020])
        chart_data.append({"n": name, "a": a, "b": b})
    chart_data.sort(key=lambda x: x["b"], reverse=True)
    print(json.dumps(chart_data, separators=(",", ":")))
    return NAME_MAP, SELECTED, chart_data, code, info


if __name__ == "__main__":
    app.run()
