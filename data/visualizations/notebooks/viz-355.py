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
        # International Tourism Arrivals 1995-2020 -- Methodology

        Trend lines for 8 top tourist destinations showing COVID-19 collapse in 2020.
        Data is in millions of international arrivals.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    SELECTED = {"CN":"China","IT":"Italy","HR":"Croatia","DE":"Germany","GR":"Greece","JP":"Japan","KR":"S. Korea","AT":"Austria"}

    country_data = {}
    for pt in data:
        code = pt["country"]
        if code not in SELECTED:
            continue
        yr = pt["year"]
        v = pt["value"]
        if v is not None:
            if code not in country_data:
                country_data[code] = {"name": SELECTED[code], "values": {}}
            country_data[code]["values"][yr] = v

    result = []
    for code, info in country_data.items():
        years = sorted(yr for yr in info["values"] if 1995 <= yr <= 2020)
        if len(years) < 20:
            continue
        pts = [{"y": yr, "v": round(info["values"][yr]/1e6, 2)} for yr in years]
        result.append({"n": info["name"], "pts": pts})

    result.sort(key=lambda x: max(p["v"] for p in x["pts"]), reverse=True)
    print(json.dumps(result, separators=(",", ":")))
    return SELECTED, code, country_data, info, result


if __name__ == "__main__":
    app.run()
