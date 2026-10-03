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
        # Stillbirth Rate: 2000 vs Recent Year — Methodology

        Slope chart comparing stillbirths per 1,000 births between 2000 and the
        most recent available year (2022 or 2023) for 16 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHOSIS_000014.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    ISO3_NAMES = {
        'AFG':'Afghanistan','BEN':'Benin','TCD':'Chad','GNB':'Guinea-Bissau',
        'JAM':'Jamaica','MDV':'Maldives','NIC':'Nicaragua','PRY':'Paraguay',
        'MNE':'Montenegro','HND':'Honduras','SSD':'South Sudan','MOZ':'Mozambique',
        'GEO':'Georgia','DOM':'Dom. Rep.','URY':'Uruguay','USA':'USA','KOR':'S. Korea'
    }

    country_data = {}
    for row in data:
        code = row['country']
        year = row['year']
        val = row['value']
        if code in ISO3_NAMES and val is not None:
            if code not in country_data:
                country_data[code] = {}
            country_data[code][year] = val

    slope = []
    for code, yd in country_data.items():
        y2000 = yd.get(2000)
        y_late = yd.get(2023) or yd.get(2022) or yd.get(2021) or yd.get(2020)
        if y2000 is not None and y_late is not None:
            slope.append({"n": ISO3_NAMES[code], "a": round(y2000, 1), "b": round(y_late, 1)})

    slope.sort(key=lambda x: x['a'], reverse=True)
    for s in slope:
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({s['b']-s['a']:+.1f})")
    return slope,


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for showing before/after across many entities
        - **Year selection**: 2000 (baseline) vs most recent year available (2022/2023)
        - **Country selection**: Countries with data at both endpoints spanning full range
        - **Color encoding**: By 2000 rate (red = high burden, green = low)
        - **Key insight**: All 16 reduced stillbirths, but high-burden countries remain >25x higher than South Korea
        """
    )
    return


@app.cell
def _(json, slope):
    import json as _json
    print(_json.dumps(slope, separators=(',',':')))
    return


if __name__ == "__main__":
    app.run()
