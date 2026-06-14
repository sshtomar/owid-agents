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
        # Primary School Completion Rate 1990-2024 -- Methodology

        Trend lines for 6 countries showing dramatic progress in primary education.
        Values capped at 100% (>100 can occur when overage students complete).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CMPT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    SELECTED = {"GT":"Guatemala","GM":"Gambia","GH":"Ghana","CV":"Cabo Verde","BT":"Bhutan","ET":"Ethiopia"}

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
        years = sorted(yr for yr in info["values"] if 1990 <= yr <= 2024)
        pts = [{"y": yr, "v": round(min(info["values"][yr], 100), 1)} for yr in years]
        result.append({"n": info["name"], "pts": pts})

    result.sort(key=lambda x: x["pts"][-1]["v"] if x["pts"] else 0, reverse=True)
    print(json.dumps(result, separators=(",", ":")))
    return SELECTED, code, country_data, info, result


if __name__ == "__main__":
    app.run()
