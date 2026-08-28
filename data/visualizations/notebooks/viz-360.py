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
        # NCD Mortality Risk — Methodology

        Documents the slope chart showing probability of dying from
        a non-communicable disease (age 30–70) in 2000 vs. 2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-NCOM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    import re
    country_data = {}
    for pt in data:
        code = pt["country"]
        if re.match(r"^[A-Z]{2}$", code) and pt["value"] is not None:
            cn = pt["countryName"]
            yr = pt["year"]
            if cn not in country_data:
                country_data[cn] = {}
            country_data[cn][yr] = pt["value"]
    both = {cn: v for cn, v in country_data.items() if 2000 in v and 2021 in v}
    ranked = sorted(both.items(), key=lambda x: -x[1].get(2021, 0))
    print(f"Countries with 2000+2021 data: {len(both)}")
    print("Highest 2021 NCD mortality:", [(cn, round(v[2021], 1)) for cn, v in ranked[:10]])
    print("Lowest 2021 NCD mortality:", [(cn, round(v[2021], 1)) for cn, v in ranked[-10:]])
    return both, cn, code, country_data, pt, ranked, re, v, yr


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two points (2000 and 2021) highlight 21-year progress
        - **Country selection**: Top 10 highest burden in 2021 + key large economies for reference
        - **Color**: Red = worsened, amber = little change, green = improved, dark green = strong improvement
        - **Story**: East Asia (Japan, Korea) has the world's lowest NCD mortality; Pacific island nations and sub-Saharan Africa remain at very high risk
        """
    )
    return


@app.cell
def _(both, json, ranked):
    top10 = dict(ranked[:10])
    notable = {cn: v for cn, v in both.items()
               if cn in ["Japan", "France", "China", "India", "Germany", "Australia", "Korea, Rep."]}
    combined = {**top10, **notable}
    chart_data = [
        {"n": cn.replace(", Arab Rep.", "").replace(", Rep.", "").replace("Central African Republic", "Central African Rep.").replace("Korea, Rep.", "Korea"),
         "a": round(v.get(2000, 0), 1),
         "b": round(v.get(2021, 0), 1)}
        for cn, v in combined.items()
    ]
    chart_data.sort(key=lambda x: -x["b"])
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, cn, combined, notable, top10, v


if __name__ == "__main__":
    app.run()
