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
        # Learning Poverty — Methodology

        Horizontal bar chart of the 30 countries with the highest learning poverty rate
        (share of children unable to read proficiently by end of primary school).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-LPV-PRIM.json"
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

    latest = {}
    for cc, rows in by_country.items():
        rows.sort(key=lambda r: r['year'])
        latest[cc] = rows[-1]

    sorted_latest = sorted(latest.values(), key=lambda r: -r['value'])
    chart_data = [{'n': r['countryName'], 'v': round(r['value'], 1), 'y': r['year']} for r in sorted_latest[:30]]
    print(f"Top 30 by learning poverty:")
    for r in chart_data:
        print(f"  {r['n']}: {r['v']}% ({r['y']})")
    return chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — easy comparison across many countries
        - **Country selection**: Top 30 with highest learning poverty (most recent survey year)
        - **Color**: Warm ramp from deep red (>90%) to amber (<50%)
        - **Key story**: Sub-Saharan Africa and parts of South/SE Asia have near-universal reading failure; Ireland and South Korea are below 4%
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
