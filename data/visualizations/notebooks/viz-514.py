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
        # Adults Who Completed Primary School — Methodology

        Sparkline grid showing share of adults 25+ with at least primary education
        completed, sorted by improvement over the observation period.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-CUAT-ZS.json"
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
    target_years = list(range(1990, 2024, 5))
    result = []

    for name, yd in by_country.items():
        avail = sorted(yd.keys())
        if max(avail) < 2015 or min(avail) > 2000:
            continue
        pts = []
        for y in target_years:
            closest = min(avail, key=lambda yr: abs(yr - y))
            if abs(closest - y) <= 4:
                pts.append({'y': y, 'v': round(yd[closest], 1)})
        if len(pts) >= 4:
            first_v = pts[0]['v']
            last_v = pts[-1]['v']
            improvement = last_v - first_v
            disp = name.replace('Korea, Rep.', 'S. Korea').replace('Dominican Republic', 'Dominican Rep.').replace('Hong Kong SAR, China', 'Hong Kong')
            result.append({
                'n': disp,
                's': [p['v'] for p in pts],
                'e': first_v,
                'l': last_v,
                'imp': round(improvement, 1),
                'y0': pts[0]['y']
            })

    result.sort(key=lambda x: -x['imp'])
    top24 = result[:24]
    print(f"Total: {len(result)}, using top 24 by improvement")
    for r in top24:
        print(f"  {r['n']}: {r['e']}% -> {r['l']}% ({r['imp']:+.1f}pp)")

    chart_data = [{'n': r['n'], 's': r['s'], 'e': r['e'], 'l': r['l'], 'y0': r['y0']} for r in top24]
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, result, target_years, top24


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — many entities, one metric over time, compact comparison
        - **Sort order**: By improvement (largest gains first) — emphasizes progress narrative
        - **Scale**: Fixed 0-100% axis so sparklines are comparable across cells
        - **Key story**: Bahrain jumped from 35% to 93%; India from 34% to 61%;
          Ethiopia still at only 26% — shows stark variation in adult education
        """
    )
    return


if __name__ == "__main__":
    app.run()
