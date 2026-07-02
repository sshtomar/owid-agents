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
        # Exclusive Breastfeeding: First Survey vs Latest Survey -- Methodology

        Slope chart comparing each country's earliest available survey (~1986-2000)
        against its most recent survey (2014-2020). Shows dramatic improvements
        in Sub-Saharan Africa and Southeast Asia alongside surprising declines in
        some Middle Eastern and Caribbean countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHOSIS_000006.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    iso3_names = {
        'LKA':'Sri Lanka','ZMB':'Zambia','KHM':'Cambodia','TGO':'Togo','BFA':'Burkina Faso',
        'GHA':'Ghana','SLE':'Sierra Leone','NGA':'Nigeria','PER':'Peru','KEN':'Kenya',
        'ZWE':'Zimbabwe','TZA':'Tanzania','SEN':'Senegal','MLI':'Mali','CMR':'Cameroon',
        'HTI':'Haiti','RWA':'Rwanda','BDI':'Burundi','UGA':'Uganda','ETH':'Ethiopia',
        'EGY':'Egypt','JOR':'Jordan','NPL':'Nepal','DOM':'Dominican Rep.',
        'BGD':'Bangladesh','IND':'India',
    }

    by_c = defaultdict(list)
    for x in data:
        if x['value'] is not None and x['country'] in iso3_names:
            by_c[x['country']].append((x['year'], round(x['value'], 1)))

    slope = []
    for c, pts in by_c.items():
        pts.sort()
        early = [(y, v) for y, v in pts if y <= 2000]
        late = [(y, v) for y, v in pts if y >= 2013]
        if early and late:
            first_yr, first_v = early[0]
            last_yr, last_v = late[-1]
            slope.append({
                'n': iso3_names[c], 'a': first_v, 'b': last_v,
                'ya': first_yr, 'yb': last_yr,
            })

    slope.sort(key=lambda x: -x['a'])
    print(f"Series: {len(slope)}")
    for s in slope:
        change = s['b'] - s['a']
        print(f"  {s['n']}: ~{s['ya']}={s['a']}% -> {s['yb']}={s['b']}% ({change:+.1f}pp)")
    return by_c, iso3_names, slope


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (earliest survey vs latest survey)
        - **Color**: Green for large gains (>20pp), amber for moderate, red for declines
        - **Story**: Sri Lanka achieved the most dramatic rise — from 10% in 1987 to 81% in 2016.
          Cambodia, Zambia, Togo, Ghana, and Sierra Leone all gained 50+ percentage points.
          Egypt (61% → 40%), Jordan (39% → 25%), and Dominican Rep. (11% → 5%) declined.
        - **Note**: Survey years vary by country; labels show approximate earliest year.
        """
    )
    return


@app.cell
def _(json, slope):
    chart_data = [{'n': d['n'], 'a': d['a'], 'b': d['b']} for d in slope]
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
