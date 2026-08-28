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
        # Tourism Arrivals COVID Impact — Methodology

        This notebook documents the data pipeline behind the slope chart
        showing international tourist arrivals in 2019 vs. 2020.
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
    both = {cn: v for cn, v in country_data.items() if 2019 in v and 2020 in v}
    ranked = sorted(both.items(), key=lambda x: -x[1][2019])[:14]
    print(f"Countries with 2019+2020 data: {len(both)}")
    print("Top 14 by 2019 arrivals:")
    for cn, v in ranked:
        drop = (v[2019] - v[2020]) / v[2019] * 100
        print(f"  {cn}: 2019={v[2019]/1e6:.1f}M, 2020={v[2020]/1e6:.1f}M, drop={drop:.0f}%")
    return both, cn, code, country_data, drop, pt, ranked, re, v, yr


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points (before/after) makes slope chart ideal
        - **Country selection**: Top 14 by 2019 arrivals that also reported 2020 data
        - **Color**: Encodes severity of drop (>85% = deep orange accent, <55% = cool green)
        - **Story**: COVID caused an unprecedented collapse, especially in East Asia where border closures were strictest
        """
    )
    return


@app.cell
def _(json, ranked):
    chart_data = [
        {"n": cn.replace(", Rep.", "").replace(" SAR, China", ""),
         "a": round(v[2019] / 1e6, 2),
         "b": round(v[2020] / 1e6, 2)}
        for cn, v in ranked
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
