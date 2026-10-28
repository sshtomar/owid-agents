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
        # Energy Vulnerability: Net Energy Imports — Methodology

        Trend lines showing net energy imports as % of energy use for 12 countries
        (Europe + China + India), 2000–2022 at 2-year intervals.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-IMP-CONS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_markers = [
        'income', 'OECD', 'IDA', 'IBRD', 'Arab', 'Fragile', 'Small',
        'Heavily', 'Least', 'Euro area', 'Monetary', 'economies', 'only',
        'zone', 'Union', 'Saharan', 'World', 'demographic', 'dividend',
        'Pacific', 'Africa', 'America', 'Asia', 'Europe', 'region',
        'Caribbean', 'South Asia', 'East Asia', 'North Africa',
        'Sub-Saharan', 'Latin', 'North America', 'countries', 'total',
        'states', 'Central'
    ]

    def is_country(name):
        return not any(a.lower() in name.lower() for a in agg_markers)

    by_country = {}
    for x in data:
        if x['value'] is not None and is_country(x['countryName']):
            cn = x['countryName']
            if cn not in by_country:
                by_country[cn] = {}
            by_country[cn][x['year']] = x['value']

    print(f"Countries: {len(by_country)}")
    return by_country, is_country


@app.cell
def _(by_country, json):
    target = [
        'Belgium', 'Ireland', 'Korea, Rep.', 'Italy', 'Greece',
        'Austria', 'Germany', 'Hungary', 'France', 'India', 'China', 'Denmark'
    ]
    years = list(range(2000, 2023, 2))

    result = []
    for name in target:
        disp = name.replace('Korea, Rep.', 'S. Korea')
        if name not in by_country:
            continue
        yd = by_country[name]
        pts = [{'y': y, 'v': round(yd[y], 1)} for y in years if y in yd and -300 < yd[y] < 300]
        if len(pts) >= 8:
            result.append({'n': disp, 'pts': pts})
            print(f"{disp}: 2000={pts[0]['v']}%, 2022={pts[-1]['v']}% ({pts[-1]['v']-pts[0]['v']:+.1f}pp)")

    print(json.dumps(result, separators=(',', ':')))
    return name, pts, result, target, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — continuous 22-year arc, shows trajectories over time
        - **Country selection**: High-import Europeans + China/India as fast-growing importers +
          Denmark as the dramatic reversal story (North Sea oil depletion)
        - **Key story**: Denmark went from -40% (exporter) to +48% (importer) as North Sea
          oil reserves depleted; China jumped from near zero to 20%; Germany's dependence
          accelerated post-2016
        - **Reference lines**: 0% (self-sufficient) and 100% (fully dependent)
        """
    )
    return


if __name__ == "__main__":
    app.run()
