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
        # Physical Inactivity Prevalence -- Methodology

        Horizontal bar chart showing the prevalence of insufficient physical activity
        among adults 18+ (age-standardized estimate) around 2021, ranked from most
        to least inactive. Data from WHO GHO.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_PAA.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    iso3_names = {
        'CYP': 'Cyprus', 'MLT': 'Malta', 'MYS': 'Malaysia', 'GRC': 'Greece',
        'GRD': 'Grenada', 'PRY': 'Paraguay', 'UZB': 'Uzbekistan', 'OMN': 'Oman',
        'URY': 'Uruguay', 'EGY': 'Egypt', 'PAK': 'Pakistan', 'HND': 'Honduras',
        'HUN': 'Hungary', 'DMA': 'Dominica', 'BEL': 'Belgium', 'MKD': 'N. Macedonia',
        'BLZ': 'Belize', 'ROU': 'Romania', 'TUR': 'Turkey', 'LCA': 'St Lucia',
        'NLD': 'Netherlands', 'CZE': 'Czechia', 'BIH': 'Bosnia', 'MUS': 'Mauritius',
        'POL': 'Poland', 'MDA': 'Moldova', 'SVK': 'Slovakia', 'KAZ': 'Kazakhstan',
        'TUN': 'Tunisia', 'AUT': 'Austria', 'CAF': 'C. Afr. Rep.', 'ERI': 'Eritrea',
        'FJI': 'Fiji', 'EST': 'Estonia', 'BFA': 'Burkina Faso', 'ZMB': 'Zambia',
        'SLB': 'Solomon Is.', 'KHM': 'Cambodia', 'DNK': 'Denmark', 'COG': 'Congo',
        'KEN': 'Kenya', 'BTN': 'Bhutan', 'FIN': 'Finland', 'NPL': 'Nepal',
        'VUT': 'Vanuatu', 'DEU': 'Germany', 'MOZ': 'Mozambique', 'COD': 'DR Congo',
        'AGO': 'Angola', 'TZA': 'Tanzania', 'SLE': 'Sierra Leone', 'BGR': 'Bulgaria',
        'SVN': 'Slovenia', 'LVA': 'Latvia', 'LTU': 'Lithuania', 'SRB': 'Serbia',
        'HRV': 'Croatia',
    }

    by_country = defaultdict(dict)
    for x in data:
        if x['value'] is not None:
            name = iso3_names.get(x['country'])
            if name:
                by_country[name][x['year']] = (x['value'], x['country'])

    chart_data = []
    for name, yrs in by_country.items():
        if 2021 in yrs:
            v, yr = yrs[2021], 2021
        elif 2020 in yrs:
            v, yr = yrs[2020], 2020
        elif 2019 in yrs:
            v, yr = yrs[2019], 2019
        else:
            continue
        chart_data.append({'n': name, 'v': round(v, 1), 'y': yr})

    chart_data.sort(key=lambda x: -x['v'])
    print(f"Countries: {len(chart_data)}")
    for c in chart_data:
        print(f"  {c['n']}: {c['v']}%")
    return chart_data, by_country, iso3_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart (ranked), allows comparing 40+ countries
        - **Color**: Gradient from red (high inactivity) to green (low inactivity)
        - **Story**: Mediterranean and Middle East countries show highest inactivity (Serbia 41%,
          Cyprus 41%, Malta 38%). Sub-Saharan Africa and Pacific islands show lowest rates.
          Physical labour context matters — lower rates in poorer countries may reflect
          occupational physical activity rather than leisure sport.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
