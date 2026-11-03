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
        # Men Are Marrying Later — Methodology

        This notebook documents the data pipeline behind viz-514.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-SMAM-MA.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    by_c = {}
    for r in data:
        if r['value'] is not None:
            by_c.setdefault(r['countryName'], {})[r['year']] = r['value']
    print(f"Countries: {len(by_c)}")
    return (by_c,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the rising trajectory across decades
        - **Country selection**: 12 countries from diverse regions (East Asia, South Asia, Europe, Africa, Americas)
        - **Time range**: 1960–2018 (full available range)
        - **Highlights**: Italian men went from age 27 in 1971 to 35 in 2018; South Korean from 27 to 34
        - **Story**: Marriage age is rising globally, driven most sharply by European and East Asian men
        """
    )
    return


@app.cell
def _(by_c, json):
    targets = {
        'South Korea': 'Korea, Rep.',
        'Italy': 'Italy',
        'Germany': 'Germany',
        'France': 'France',
        'Japan': 'Japan',
        'China': 'China',
        'India': 'India',
        'Bangladesh': 'Bangladesh',
        'Brazil': 'Brazil',
        'Colombia': 'Colombia',
        'Ghana': 'Ghana',
        'Ethiopia': 'Ethiopia',
    }
    out = []
    for display_name, lookup_name in targets.items():
        if lookup_name in by_c:
            ys = by_c[lookup_name]
            pts = [{"y": yr, "v": round(val, 1)} for yr, val in sorted(ys.items())]
            out.append({"n": display_name, "pts": pts})
    print(json.dumps(out, separators=(",", ":")))
    return out, targets


if __name__ == "__main__":
    app.run()
