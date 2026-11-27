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
        # Mean Fasting Blood Glucose — Methodology

        Horizontal bar chart showing top 20 highest and bottom 10 lowest countries
        by age-standardized mean fasting blood glucose (mmol/L). Most recent survey
        year used per country (1980–2014 window).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_GLUC_01.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso3_map = {
        'PLW': 'Palau', 'MHL': 'Marshall Is.', 'COK': 'Cook Islands',
        'KIR': 'Kiribati', 'TON': 'Tonga', 'SAU': 'Saudi Arabia',
        'VUT': 'Vanuatu', 'WSM': 'Samoa', 'FSM': 'Micronesia', 'TUV': 'Tuvalu',
        'DMA': 'Dominica', 'NIU': 'Niue', 'FJI': 'Fiji', 'SYC': 'Seychelles',
        'PNG': 'Papua N. Guinea', 'GEO': 'Georgia', 'QAT': 'Qatar',
        'MUS': 'Mauritius', 'BTN': 'Bhutan', 'SLB': 'Solomon Is.',
        'HTI': 'Haiti', 'UGA': 'Uganda', 'ERI': 'Eritrea', 'TGO': 'Togo',
        'PRT': 'Portugal', 'TLS': 'Timor-Leste', 'KHM': 'Cambodia',
        'RWA': 'Rwanda', 'BDI': 'Burundi', 'MOZ': 'Mozambique',
    }
    latest = {}
    for row in data:
        if row['value'] is None:
            continue
        code = row['country']
        name = iso3_map.get(code, code)
        if name not in latest or row['year'] > latest[name][0]:
            latest[name] = (row['year'], round(row['value'], 3))

    ranked = sorted(latest.items(), key=lambda x: -x[1][1])
    print(f"Total countries: {len(ranked)}")
    print("Top 5:", [(n, v) for n, (yr, v) in ranked[:5]])
    print("Bottom 5:", [(n, v) for n, (yr, v) in ranked[-5:]])
    return iso3_map, latest, ranked


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — clear ranking comparison
        - **Selection**: Top 20 high + bottom 10 low to show global extremes
        - **Color**: By geographic region (Pacific red, Gulf amber, Africa green)
        - **Insight**: Pacific Islands dominate the top — dietary transition from traditional foods
        - **Threshold**: 5.6 mmol/L marked as pre-diabetic reference line
        """
    )
    return


@app.cell
def _(json, ranked):
    region_map = {
        'Palau': 'Pacific', 'Marshall Is.': 'Pacific', 'Cook Islands': 'Pacific',
        'Kiribati': 'Pacific', 'Tonga': 'Pacific', 'Vanuatu': 'Pacific',
        'Samoa': 'Pacific', 'Micronesia': 'Pacific', 'Tuvalu': 'Pacific',
        'Niue': 'Pacific', 'Fiji': 'Pacific', 'Papua N. Guinea': 'Pacific',
        'Solomon Is.': 'Pacific', 'Saudi Arabia': 'Gulf', 'Qatar': 'Gulf',
        'Georgia': 'Europe/C.Asia', 'Mauritius': 'Africa', 'Seychelles': 'Africa',
        'Bhutan': 'S.Asia', 'Dominica': 'Caribbean',
        'Haiti': 'Caribbean', 'Uganda': 'Africa', 'Eritrea': 'Africa',
        'Togo': 'Africa', 'Rwanda': 'Africa', 'Burundi': 'Africa',
        'Mozambique': 'Africa', 'Portugal': 'Europe',
        'Timor-Leste': 'Other', 'Cambodia': 'SE.Asia',
    }
    top20 = [{"n": n, "v": v, "r": region_map.get(n, 'Other')} for n, (_, v) in ranked[:20]]
    bot10 = [{"n": n, "v": v, "r": region_map.get(n, 'Other')} for n, (_, v) in ranked[-10:]]
    print("Top 20:")
    print(json.dumps(top20, separators=(",", ":")))
    print("\nBottom 10:")
    print(json.dumps(bot10, separators=(",", ":")))
    return bot10, region_map, top20


if __name__ == "__main__":
    app.run()
