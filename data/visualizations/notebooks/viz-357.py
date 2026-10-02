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
        # Hypertension Treatment Coverage — Methodology

        Horizontal bar chart showing the most recent available treatment coverage
        for hypertension across 40 countries, illustrating the ~20x global gap.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_HYP_TREATMENT_A.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip = {'AFR','AMR','EMR','EUR','SEA','WPR','LMI','UMI','LIC','HIC','MIC','WLD','GLOBAL',
            'G20','G7','PRI','GUM','VIR','ASM','MNP','TKL','AND','LIE','MCO','SMR','VAT'}
    filtered = [r for r in data if r['country'] not in skip and r['value'] is not None
                and 'UNSDG' not in r['country']]
    print(f"After filtering aggregates: {len(filtered)} records")
    return (filtered,)


@app.cell
def _(filtered):
    # Most recent value per country
    most_recent = {}
    for r in filtered:
        cc = r['country']
        if cc not in most_recent or r['year'] > most_recent[cc]['year']:
            most_recent[cc] = r
    vals = sorted(most_recent.values(), key=lambda x: x['value'])
    print(f"Countries with data: {len(vals)}")
    print(f"Value range: {vals[0]['value']:.1f}% - {vals[-1]['value']:.1f}%")
    return most_recent, vals


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — single-year cross-country comparison
        - **Country selection**: 40 countries spanning the full value range: bottom 12, 13 middle, top 15
        - **Measurement years**: Most recent available per country (varies 2000–2019)
        - **Highlights**: Niger at 4%, South Korea at 77.5% — a 20-fold gap
        """
    )
    return


@app.cell
def _(json, vals):
    iso_names = {
        'NER':'Niger','VUT':'Vanuatu','TZA':'Tanzania','ETH':'Ethiopia','CMR':'Cameroon',
        'IDN':'Indonesia','RWA':'Rwanda','KEN':'Kenya','GAB':'Gabon','GIN':'Guinea',
        'MOZ':'Mozambique','NGA':'Nigeria','UGA':'Uganda','GMB':'Gambia','ARM':'Armenia',
        'BIH':'Bosnia','MDA':'Moldova','LKA':'Sri Lanka','URY':'Uruguay','ARG':'Argentina',
        'VEN':'Venezuela','PRT':'Portugal','KWT':'Kuwait','EGY':'Egypt','MLT':'Malta',
        'DOM':'Dominican Rep.','SGP':'Singapore','SVK':'Slovakia','BHS':'Bahamas',
        'MNG':'Mongolia','SYC':'Seychelles','JAM':'Jamaica','DEU':'Germany','ROU':'Romania',
        'NIC':'Nicaragua','USA':'USA','CUB':'Cuba','ISL':'Iceland','CRI':'Costa Rica',
        'KOR':'South Korea'
    }
    top = vals[-15:]
    bottom = vals[:12]
    mid_pool = vals[12:-15]
    step = max(1, len(mid_pool) // 13)
    mid = mid_pool[::step][:13]
    selected = sorted(set([v['country'] for v in bottom + mid + top]))
    selected_records = [most_recent[cc] for cc in selected if cc in most_recent]
    selected_records.sort(key=lambda x: x['value'])
    chart_data = [
        {"n": iso_names.get(r['country'], r['country']), "v": round(r['value'],1), "y": r['year']}
        for r in selected_records if r['country'] in iso_names
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
