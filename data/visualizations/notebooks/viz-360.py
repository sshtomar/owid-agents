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
        # Depression Prevalence 2015 — Methodology

        Bar chart showing estimated population-based depression prevalence across
        183 countries. Top 15 (highest) and bottom 15 (lowest) selected.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--GDO_q35.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points (all 2015)")
    return data, raw


@app.cell
def _(data):
    iso_names = {
        'UKR':'Ukraine','AUS':'Australia','EST':'Estonia','BRA':'Brazil','GRC':'Greece',
        'PRT':'Portugal','LTU':'Lithuania','FIN':'Finland','BLR':'Belarus','RUS':'Russia',
        'CUB':'Cuba','MDA':'Moldova','NZL':'New Zealand','BRB':'Barbados','PRY':'Paraguay',
        'USA':'USA','EGY':'Egypt','NER':'Niger','KHM':'Cambodia','PHL':'Philippines',
        'AFG':'Afghanistan','NPL':'Nepal','LAO':'Laos','TON':'Tonga','WSM':'Samoa',
        'FSM':'Micronesia','KIR':'Kiribati','VUT':'Vanuatu','TLS':'Timor-Leste',
        'PNG':'Papua NG','SLB':'Solomon Isl.'
    }
    filtered = [r for r in data if r['value'] is not None and r['country'] in iso_names]
    for r in filtered:
        r['displayName'] = iso_names[r['country']]
    filtered.sort(key=lambda x: x['value'], reverse=True)
    print(f"Countries with names: {len(filtered)}")
    print(f"Range: {filtered[-1]['value']:.2f}% - {filtered[0]['value']:.2f}%")
    return (filtered,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar, split into two sections (highest / lowest)
        - **Country selection**: 15 highest + 15 lowest = 30 countries
        - **Story**: Eastern European / post-Soviet countries cluster at the top; Pacific Islands at bottom
        - **Note**: Estimates reflect methodological differences, not just underlying burden
        """
    )
    return


@app.cell
def _(filtered, json):
    selected = filtered[:15] + filtered[-15:]
    selected.sort(key=lambda x: x['value'], reverse=True)
    chart_data = [{"n": r['displayName'], "v": round(r['value'],2)} for r in selected]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
