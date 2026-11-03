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
        # Women's Share of HIV in Sub-Saharan Africa — Methodology

        This notebook documents the data pipeline behind viz-511.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-AIDS-FE-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_names = ['Eastern', 'Western', 'South Asia', 'East Asia', 'Sub-Saharan',
                 'Arab World', 'Euro area', 'European Union', 'OECD', 'World', 'income',
                 'IDA', 'IBRD', 'Caribbean', 'Fragility', 'dividend', 'states',
                 'Latin America', 'Middle East', 'North America', 'Pacific', 'Saharan',
                 'Heavily indebted', 'Least developed', 'classification', 'FCV']
    real = [r for r in data if r['value'] is not None and
            not any(w in r['countryName'] for w in agg_names)]
    by_c = {}
    for r in real:
        by_c.setdefault(r['countryName'], {})[r['year']] = r['value']
    print(f"Real countries: {len(by_c)}")
    return agg_names, by_c, real


@app.cell
def _(by_c):
    latest_val = {}
    for c, ys in by_c.items():
        latest_year = max(ys.keys())
        if latest_year >= 2022:
            latest_val[c] = ys[latest_year]
    top12 = sorted(latest_val.items(), key=lambda x: -x[1])[:12]
    print("Top 12 countries by female HIV share (2024):")
    for c, v in top12:
        print(f"  {c}: {v:.1f}%")
    return latest_val, top12


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows how the female share has changed continuously from 1990 to 2024
        - **Country selection**: Top 12 sub-Saharan African countries by latest female HIV share
        - **Time range**: 1990–2024 (full series since UNAIDS estimates begin)
        - **Highlights**: Every country shown has >60% female share; most are increasing
        - **Story**: HIV has become increasingly feminized — women bear a disproportionate and growing burden
        """
    )
    return


@app.cell
def _(by_c, json, top12):
    out = []
    for c, _ in top12:
        ys = by_c[c]
        pts = [{"y": yr, "v": round(val, 1)} for yr, val in sorted(ys.items())]
        out.append({"n": c, "pts": pts})
    print(json.dumps(out, separators=(",", ":")))
    return (out,)


if __name__ == "__main__":
    app.run()
