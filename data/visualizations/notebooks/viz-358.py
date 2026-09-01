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
        # COVID-19 Tourism Collapse — Methodology

        Slope chart comparing international tourist arrivals in 2019 (pre-COVID peak) vs 2020 (COVID year).
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
    targets = {
        'France': 'France', 'China': 'China', 'Italy': 'Italy',
        'Hungary': 'Hungary', 'Croatia': 'Croatia',
        'Hong Kong SAR, China': 'Hong Kong', 'Germany': 'Germany',
        'Greece': 'Greece', 'Japan': 'Japan',
        'Korea, Rep.': 'S. Korea', 'Indonesia': 'Indonesia'
    }
    d19 = {r['countryName']: r['value'] for r in data if r['year'] == 2019 and r['countryName'] in targets and r['value'] is not None}
    d20 = {r['countryName']: r['value'] for r in data if r['year'] == 2020 and r['countryName'] in targets and r['value'] is not None}
    print(f"Countries with 2019 data: {len(d19)}, with 2020 data: {len(d20)}")
    return d19, d20, targets


@app.cell
def _(d19, d20, targets):
    chart_data = []
    for orig, disp in sorted(targets.items(), key=lambda x: -d19.get(x[0], 0)):
        if orig in d19 and orig in d20:
            a = round(d19[orig] / 1e6, 1)
            b = round(d20[orig] / 1e6, 1)
            pct = (b - a) / a * 100
            chart_data.append({"n": disp, "a": a, "b": b})
            print(f"  {disp}: {a}M -> {b}M ({pct:.0f}%)")
    return chart_data,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparison across many entities
        - **Year choice**: 2019 (pre-COVID peak) vs 2020 (first COVID year)
        - **Color encoding**: Intensity of decline — deeper red for 80%+ drops (Hong Kong -94%, Japan -87%)
        - **Key story**: Every major tourism destination saw catastrophic drops; Hong Kong and Asian destinations hit hardest
        - **Label collision**: resolveCollisions() applied to both left and right label sets with 13px min gap
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
