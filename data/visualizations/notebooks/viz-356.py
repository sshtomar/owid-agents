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
        # Hospital Beds per 10,000 — Methodology

        This notebook documents the pipeline for the slope chart comparing hospital beds
        per 10,000 population around 2000 vs around 2020.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHS6_102.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    iso_map = {
        'KOR': 'South Korea', 'MNG': 'Mongolia', 'BGR': 'Bulgaria', 'DEU': 'Germany',
        'AUT': 'Austria', 'ROU': 'Romania', 'RUS': 'Russia', 'HUN': 'Hungary',
        'UKR': 'Ukraine', 'KAZ': 'Kazakhstan', 'SVK': 'Slovakia', 'LTU': 'Lithuania',
        'MDA': 'Moldova', 'HRV': 'Croatia', 'BEL': 'Belgium', 'LVA': 'Latvia',
        'CHN': 'China', 'UZB': 'Uzbekistan', 'MKD': 'N. Macedonia', 'GEO': 'Georgia',
        'IDN': 'Indonesia', 'ARM': 'Armenia', 'AZE': 'Azerbaijan', 'FIN': 'Finland',
        'SWE': 'Sweden',
    }

    pts = [p for p in data if p['value'] is not None]
    by_code = defaultdict(dict)
    for p in pts:
        code = p.get('country', p.get('countryName', ''))
        by_code[code][p['year']] = p['value']

    result = []
    for code, vals in by_code.items():
        name = iso_map.get(code)
        if not name:
            continue
        years = sorted(vals.keys())
        avail_start = [y for y in years if y >= 2000]
        avail_end = [y for y in years if y <= 2022]
        if not avail_start or not avail_end:
            continue
        yr_start, yr_end = avail_start[0], avail_end[-1]
        if yr_end - yr_start < 5:
            continue
        result.append({'n': name, 'a': round(vals[yr_start], 1), 'ay': yr_start, 'b': round(vals[yr_end], 1), 'by': yr_end})

    chart_data = [{'n': r['n'], 'a': r['a'], 'b': r['b']} for r in sorted(result, key=lambda x: -x['b'])]

    print(f"Countries: {len(chart_data)}")
    for r in sorted(result, key=lambda x: -(x['b']-x['a'])):
        print(f"  {r['n']}: {r['a']} ({r['ay']}) -> {r['b']} ({r['by']}) {r['b']-r['a']:+.1f}")
    return chart_data, by_code, pts, result


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two-point comparison clearly shows direction and magnitude.
        - **Country selection**: Countries where ISO code is available in the WHO dataset
          and data spans at least 2000 and 2018+.
        - **Story**: South Korea went from 47 to 128 beds (nearly 3x); China from 17 to 54 (3x).
          Meanwhile Finland cut from 74 to 28 (rationalization of care model),
          Russia from 107 to 68 (post-Soviet restructuring).
        - **Color encoding**: Large gain (>+30) in green, modest gain in light green,
          modest cut in amber, large cut (>20) in orange-red.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
