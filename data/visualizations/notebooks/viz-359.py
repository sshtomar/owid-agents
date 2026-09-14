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
        # International Tourism Arrivals — Methodology

        Trend lines for the 12 largest tourism destinations, showing the COVID-19 collapse in 2020.
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
    from collections import defaultdict

    AGGREGATES = {
        '1A','1W','4E','7E','8S','B8','EU','OE',
        'S1','S2','S3','S4','T2','T3','T4','T5','T6','T7',
        'V1','V2','V3','V4',
        'XC','XD','XE','XF','XG','XH','XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU',
        'Z4','Z7','ZF','ZG','ZH','ZI','ZJ','ZQ','ZT'
    }

    def is_country(code):
        if any(c.isdigit() for c in code):
            return False
        if code[0] == 'X':
            return False
        return code not in AGGREGATES

    by_country = defaultdict(list)
    for row in data:
        if is_country(row['country']) and row['value'] is not None:
            by_country[row['country']].append(row)

    top2019 = {cc: next(r['value'] for r in rows if r['year'] == 2019)
               for cc, rows in by_country.items()
               if any(r['year'] == 2019 for r in rows)}

    top_countries = sorted(top2019, key=lambda c: -top2019[c])[:12]
    chart_data = []
    for cc in top_countries:
        rows = sorted(by_country[cc], key=lambda r: r['year'])
        pts = [{'y': r['year'], 'v': round(r['value']/1e6, 2)} for r in rows]
        chart_data.append({'n': by_country[cc][0]['countryName'], 'pts': pts})

    print(f"Top 12 destinations. Countries: {[s['n'] for s in chart_data]}")
    return chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows time trajectory with hover isolation
        - **Country selection**: Top 12 by 2019 arrivals
        - **Key story**: Hong Kong lost 94% of visitors in 2020; China lost 81%; France and Italy lost ~50%
        - **Annotation**: Vertical marker at 2020 to highlight the COVID cliff
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
