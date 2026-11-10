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
        # Logistics Performance Index: Overall Score — Methodology

        Slope chart comparing top-25 economies' LPI scores from 2007 to 2022.
        Source dataset: wb--LP-LPI-OVRL-XQ
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--LP-LPI-OVRL-XQ.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    country_data = {}
    for p in data:
        if p["value"] is None:
            continue
        cn = p["countryName"]
        yr = p["year"]
        country_data.setdefault(cn, {})[yr] = p["value"]

    skip_words = ["income","Africa","Asia","Europe","America","World","OECD","dividend","Arab","states","IDA","IBRD","South","North","East","West","Central","Caribbean","Euro area","European"]
    result = {}
    for k, v in country_data.items():
        if any(w in k for w in skip_words):
            continue
        if 2007 in v and 2022 in v:
            result[k] = {"a": round(v[2007], 3), "b": round(v[2022], 3)}

    top = sorted(result.items(), key=lambda x: x[1]["b"], reverse=True)[:25]
    chart_data = [{"n": n, "a": v["a"], "b": v["b"]} for n, v in top]
    print(f"Countries selected: {len(chart_data)}")
    print(f"Score range 2022: {min(v['b'] for v in result.values()):.2f} – {max(v['b'] for v in result.values()):.2f}")
    return chart_data, country_data, result, top


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparison across many entities
        - **Year selection**: 2007 (first survey year) vs 2022 (most recent)
        - **Country selection**: Top 25 by 2022 score, excluding regional aggregates
        - **Color**: By improvement magnitude (green = large improvement, amber = stable, red = decline)
        - **Highlights**: Finland and China both improved strongly; Japan and Ireland slightly declined
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
