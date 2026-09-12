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
        # Energy Intensity — Methodology

        Slope chart comparing MJ per PPP GDP in 2000 vs 2020 for 25 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-EGY-PRIM-PP-KD.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    EXCLUDE = {'Europe', 'Central', 'Africa', 'Asia', 'World', 'income', 'America',
               'states', 'countries', 'Caribbean', 'Small', 'Pacific', 'Atlantic',
               'dividend', 'Fragile', 'Heavily', 'IDA', 'IBRD', 'Late', 'OECD', 'Sub',
               'North America', 'Latin', 'Arab', 'Middle', 'Euro', 'Other', 'Low',
               'Upper', 'Lower', 'High', 'Pre', 'Post', 'Developing', 'Least', 'East', 'SAR'}

    by_country = {}
    for p in data:
        cn = p["countryName"]
        y = p["year"]
        v = p["value"]
        if v is None:
            continue
        if y not in (2000, 2020):
            continue
        if any(x in cn for x in EXCLUDE):
            continue
        if cn not in by_country:
            by_country[cn] = {}
        by_country[cn][y] = round(v, 2)

    good = {k: v for k, v in by_country.items() if 2000 in v and 2020 in v}
    print(f"Countries with both years: {len(good)}")

    improvements = sorted(good.items(), key=lambda x: (x[1][2020] - x[1][2000]) / x[1][2000])
    print("Top 5 most improved:")
    for c, v in improvements[:5]:
        pct = (v[2020] - v[2000]) / v[2000] * 100
        print(f"  {c}: {v[2000]} -> {v[2020]} ({pct:+.0f}%)")
    return by_country, good, improvements


@app.cell
def _(good):
    sorted_by_2000 = sorted(good.items(), key=lambda x: -x[1][2000])
    chart_data = [{"n": c, "a": v[2000], "b": v[2020]} for c, v in sorted_by_2000[:25]]
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — before/after comparison at two time points
        - **Country selection**: 25 most energy-intensive in 2000 (excludes aggregates)
        - **Color encoding**: % reduction magnitude using diverging ramp
        - **Highlights**: Former Soviet states, developing nations show largest cuts
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
