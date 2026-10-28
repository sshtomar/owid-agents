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
        # The Service Economy — Methodology

        Trend lines showing services value added (% of GDP) for 8 major economies,
        1990–2022 at 2-year intervals.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-SRV-TOTL-ZS.json"
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
    years = list(range(1990, 2023, 2))
    target = ['France', 'Japan', 'Germany', 'S. Korea', 'Brazil', 'China', 'India', 'Indonesia']
    name_map = {'S. Korea': 'Korea, Rep.'}

    result = []
    for disp_name in target:
        lookup = name_map.get(disp_name, disp_name)
        if lookup not in by_country:
            print(f"Missing: {lookup}")
            continue
        yd = by_country[lookup]
        pts = [{'y': y, 'v': round(yd[y], 1)} for y in years if y in yd]
        if len(pts) >= 10:
            result.append({'n': disp_name, 'pts': pts})
            print(f"{disp_name}: {pts[0]['v']}% ({pts[0]['y']}) -> {pts[-1]['v']}% ({pts[-1]['y']})")

    print(json.dumps(result, separators=(',', ':')))
    return name_map, pts, result, target, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — continuous time series, 8 entities, shows trajectories
        - **Country selection**: Mix of high-service (France, Japan) and rapidly transitioning
          (China, India); Korea and Indonesia show intermediate paths
        - **Key story**: China's service sector nearly doubled from 33% to 55% — fastest expansion;
          France plateau at ~70% represents a post-industrial ceiling
        """
    )
    return


if __name__ == "__main__":
    app.run()
