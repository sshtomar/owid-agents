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
        # Rising Mean BMI — Methodology

        Slope chart comparing mean age-standardized BMI from the mid-1970s to
        the most recent available year (~2012–2016) for the 20 countries
        with the steepest rise.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_BMI_MEAN.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    ISO3_NAMES = {
        'AFG':'Afghanistan','AGO':'Angola','BWA':'Botswana','CMR':'Cameroon',
        'COM':'Comoros','CPV':'Cape Verde','CRI':'Costa Rica','GHA':'Ghana',
        'GMB':'Gambia','HND':'Honduras','KAZ':'Kazakhstan','KGZ':'Kyrgyzstan',
        'LBR':'Liberia','MEX':'Mexico','MYS':'Malaysia','PER':'Peru',
        'SUR':'Suriname','SYC':'Seychelles','TJK':'Tajikistan','TTO':'Trinidad & Tobago',
        'UGA':'Uganda','USA':'United States'
    }

    by_country = {}
    for row in data:
        cc = row.get('country', '')
        if cc == 'GLOBAL':
            continue
        year = row.get('year', 0)
        val = row.get('value')
        if val is None:
            continue
        if cc not in by_country:
            by_country[cc] = {}
        by_country[cc][year] = round(val, 1)

    slope = []
    for cc, yrs in by_country.items():
        early = [y for y in yrs if y <= 1980]
        late = [y for y in yrs if y >= 2012]
        if early and late:
            a_yr = min(early)
            b_yr = max(late)
            name = ISO3_NAMES.get(cc, cc)
            slope.append({
                'code': cc, 'n': name,
                'a': yrs[a_yr], 'b': yrs[b_yr],
                'change': round(yrs[b_yr] - yrs[a_yr], 1)
            })

    chart_data = [
        {'n': s['n'], 'a': s['a'], 'b': s['b']}
        for s in sorted(slope, key=lambda x: -x['change'])[:20]
    ]
    print(f"Countries with early+late data: {len(slope)}")
    return chart_data, slope, by_country, ISO3_NAMES


@app.cell
def _(chart_data):
    changes = [d['b'] - d['a'] for d in chart_data]
    print(f"BMI change range: {min(changes):.1f} – {max(changes):.1f} kg/m²")
    above_25 = sum(1 for d in chart_data if d['b'] >= 25)
    print(f"Countries above overweight threshold (25) by recent year: {above_25}/{len(chart_data)}")
    return changes, above_25


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — early vs late BMI for steepest risers
        - **Country selection**: Top 20 by absolute increase in mean BMI
        - **Reference line**: Overweight threshold at BMI 25 shown with shaded band
        - **Story**: Many developing nations crossed into overweight territory since 1975
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
