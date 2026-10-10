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
        # Electronic Waste by Region, 2010–2023 — Methodology

        Dataset: sdg--12-4-2--EN_EWT_GENV (UN SDG 12.4.2)
        Indicator: Electronic waste generated, total tonnes by major world region, 2010–2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--12-4-2--EN_EWT_GENV.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    regions = ['Asia', 'Americas', 'Europe', 'Africa', 'Oceania']
    result = {}
    for r in regions:
        series = sorted(
            [d for d in data if d['countryName'] == r and d['value'] is not None and 2010 <= d['year'] <= 2023],
            key=lambda x: x['year']
        )
        vals = [round(d['value'] / 1e6, 2) for d in series]
        result[r] = {'y0': 2010, 'step': 1, 's': vals}
        print(f"{r}: {len(vals)} points, 2010={vals[0]:.2f}M → 2023={vals[-1]:.2f}M tonnes")
    return (result,)


@app.cell
def _(json, result):
    chart_data = [
        {"n": k, "y0": v["y0"], "step": v["step"], "s": v["s"]}
        for k, v in result.items()
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
