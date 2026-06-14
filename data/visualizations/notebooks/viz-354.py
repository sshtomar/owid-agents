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
        # Financial Inclusion: Bank Account Ownership (2011 vs 2021) -- Methodology

        Slope chart showing the share of adults (15+) with a bank or mobile-money account
        across 20 countries, comparing 2011 to 2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FX-OWN-TOTL-ZS.json"
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
        "Egypt, Arab Rep.": "Egypt",
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "S. Korea",
        "Congo, Rep.": "Congo (Rep.)",
        "Hong Kong SAR, China": "Hong Kong",
    }
    SELECTED = [
        "AF","IQ","EG","GN","KH","BF","CM","ID","IN","GA",
        "BO","GH","AR","KE","BR","CN","HU","DE","JP","AU"
    ]

    country_vals = {}
    for pt in data:
        code = pt["country"]
        if code in AGGREGATE_CODES or code not in SELECTED:
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
        if 2011 in info["values"] and 2021 in info["values"]:
            chart_data.append({
                "n": info["name"],
                "a": round(info["values"][2011], 1),
                "b": round(info["values"][2021], 1)
            })
    chart_data.sort(key=lambda x: x["b"], reverse=True)
    print(json.dumps(chart_data, separators=(",", ":")))
    return AGGREGATE_CODES, NAME_MAP, SELECTED, chart_data, code, country_vals, info


if __name__ == "__main__":
    app.run()
