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
        # Out-of-Pocket Health Expenditure (% of Current Health Spending) — Methodology

        Slope chart comparing 2000 vs 2022/2023 values for the 30 highest-burden countries.
        Shows which countries have improved (lower OOP) vs deteriorated.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-OOPC-CH-ZS.json"
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

    chart_data = []
    for cc, rows in by_country.items():
        rows.sort(key=lambda r: r['year'])
        a_val = next((r['value'] for r in rows if r['year'] in (2000, 2001)), None)
        b_val = next((r['value'] for r in reversed(rows) if r['year'] in (2023, 2022)), None)
        if a_val is not None and b_val is not None:
            name = rows[0]['countryName']
            name = name.replace('Egypt, Arab Rep.', 'Egypt').replace('Iran, Islamic Rep.', 'Iran')
            chart_data.append({'n': name, 'a': round(a_val, 1), 'b': round(b_val, 1)})

    chart_data.sort(key=lambda x: -x['b'])
    top30 = chart_data[:30]
    print(f"Countries with data for both years: {len(chart_data)}, showing top 30")
    return top30, chart_data


@app.cell
def _(top30, mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows each country's journey from 2000 to 2022/2023
        - **Country selection**: Top 30 by most recent OOP %, showing highest-burden countries
        - **Color encoding**: Red = OOP increased (worse), green = OOP decreased (improved)
        - **Key story**: Armenia & Bangladesh now above 80%; India improved dramatically from 72% to 44%
        """
    )
    return


@app.cell
def _(top30, json):
    print(json.dumps(top30, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
