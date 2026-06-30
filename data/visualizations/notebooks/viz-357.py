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
        # UHC Service Coverage Index — Methodology

        Slope chart comparing each country's earliest available UHC index value (~2000–2005)
        with its most recent value (~2019–2023).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--UHC_INDEX_REPORTED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [p for p in data if p["value"] is not None]
    print(f"Non-null rows: {len(filtered)}")
    return (filtered,)


@app.cell
def _(filtered):
    by_country = {}
    for p in filtered:
        c = p["countryName"]
        if c not in by_country:
            by_country[c] = {}
        by_country[c][p["year"]] = p["value"]

    skip = {"SEAR","WB_EAP","WB_LI","WB_UMI","EUR","AMR","AFR","EMR","WPR","GLOBAL","WB_HI","WB_LMI"}
    names = {
        "RWA":"Rwanda","IND":"India","NPL":"Nepal","MWI":"Malawi","UGA":"Uganda",
        "GNQ":"Equatorial Guinea","LBR":"Liberia","GIN":"Guinea","ETH":"Ethiopia","PAK":"Pakistan",
        "BTN":"Bhutan","CHN":"China","CUB":"Cuba","NOR":"Norway","JPN":"Japan",
        "GBR":"UK","BEL":"Belgium","NZL":"New Zealand","CAN":"Canada","NER":"Niger",
    }

    slope = []
    for code, display in names.items():
        if code in skip or code not in by_country:
            continue
        early = [y for y in by_country[code] if y <= 2005]
        late = [y for y in by_country[code] if y >= 2019]
        if not early or not late:
            continue
        ea = max(early)
        la = max(late)
        slope.append({"n": display, "a": round(by_country[code][ea], 1), "b": round(by_country[code][la], 1)})

    slope.sort(key=lambda x: x["a"])
    print(f"Countries in slope chart: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']} -> {s['b']} (+{s['b']-s['a']:.0f})")
    return (slope,)


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
