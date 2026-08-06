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
        # Fossil Fuel Electricity Slope Chart — Methodology

        Compares the share of electricity produced from fossil fuels in 2000 vs 2022 for 14 countries.
        Countries are colored by the magnitude of their decline, revealing widely divergent energy transitions.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-FOSL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    by_country = defaultdict(list)
    for pt in data:
        if pt["value"] is not None:
            by_country[pt["countryName"]].append((pt["year"], pt["value"]))
    return by_country, defaultdict


@app.cell
def _(by_country, json):
    skip_words = ["IDA","IBRD","demographic","income","excluding","& Central","& Pacific","& Caribbean",
        "total","Fragile","Least","HIPC","island","Other small","Arab World","Euro area",
        "European Union","Central Europe","North Africa","Sub-Saharan","South Asia","North America",
        "Latin America","Eastern and Southern","Western and Central","World","OECD","small states"]
    slopes = []
    for c, v_list in by_country.items():
        if any(sw in c for sw in skip_words):
            continue
        all_pts = {y: v for y, v in v_list}
        v2000 = all_pts.get(2000)
        v2022 = all_pts.get(2022)
        if v2000 is not None and v2022 is not None:
            slopes.append({"n": c, "a": round(v2000, 1), "b": round(v2022, 1)})

    slopes.sort(key=lambda x: x["a"] - x["b"], reverse=True)
    selected_names = {"Chad","Eritrea","Iran, Islamic Rep.","Jamaica","Israel","Ireland","Cambodia","Australia","Greece","Estonia","Czechia","Denmark","Kenya","Eswatini"}
    chart_data = [s for s in slopes if s["n"] in selected_names]
    chart_data.sort(key=lambda x: -x["a"])
    print(f"Chart data ({len(chart_data)} countries):")
    for row in chart_data:
        print(f"  {row['n']}: {row['a']}% -> {row['b']}% ({row['b']-row['a']:+.1f}pp)")
    print(json.dumps(chart_data, separators=(",", ":")))
    return c, chart_data, selected_names, slopes, v2000, v2022, v_list


if __name__ == "__main__":
    app.run()
