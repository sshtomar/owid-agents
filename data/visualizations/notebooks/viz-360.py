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
        # Government Health Expenditure — Methodology

        Slope chart comparing government health spending as % of GDP in 2000 vs 2022.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-GHED-GD-ZS.json"
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
        if y not in (2000, 2022):
            continue
        if any(x in cn for x in EXCLUDE):
            continue
        if cn not in by_country:
            by_country[cn] = {}
        by_country[cn][y] = round(v, 2)

    good = {k: v for k, v in by_country.items() if 2000 in v and 2022 in v}
    print(f"Countries with both years: {len(good)}")

    sorted_c = sorted(good.items(), key=lambda x: -x[1][2022])
    print("Top 5 highest in 2022:")
    for c, v in sorted_c[:5]:
        print(f"  {c}: {v[2000]}% -> {v[2022]}%")
    return by_country, good, sorted_c


@app.cell
def _(sorted_c):
    MAJOR = {'Japan', 'Cuba', 'Germany', 'France', 'Austria', 'Denmark', 'Canada',
             'Australia', 'Brazil', 'China', 'Indonesia', 'India', 'Ethiopia',
             'Bangladesh', 'Haiti'}

    chart_data = []
    for c, v in sorted_c:
        if c in MAJOR:
            chart_data.append({"n": c, "a": v[2000], "b": v[2022]})
    chart_data.sort(key=lambda x: -x["b"])
    print(f"Chart data: {len(chart_data)} countries")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — 2-point comparison highlights change magnitude
        - **Country selection**: Mix of high-income (Japan, Germany) and low-income (Haiti, Bangladesh) for contrast
        - **Color encoding**: Change in percentage points; warm tones for gains >2pp
        - **Highlights**: Japan's aging-driven surge, China's tripling from low base, persistent low investment in low-income countries
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
