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
        # HPV Vaccination Coverage Among Girls (9-14 years), 2024 -- Methodology

        Horizontal bar chart showing HPV vaccine coverage across 42 countries in 2024.
        Highlights unexpected leaders (Burkina Faso, Uzbekistan) and surprising laggards
        (Japan with only 17%, Philippines 5%, Morocco 3%).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--SDGHPVRECEIVED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso3_names = {
        'AFG':'Afghanistan','AGO':'Angola','ALB':'Albania','AUS':'Australia','AUT':'Austria',
        'AZE':'Azerbaijan','BEL':'Belgium','BEN':'Benin','BFA':'Burkina Faso','BGD':'Bangladesh',
        'BGR':'Bulgaria','BLR':'Belarus','BRA':'Brazil','BTN':'Bhutan','CAN':'Canada',
        'CHE':'Switzerland','CHL':'Chile','CMR':'Cameroon','COL':'Colombia','CRI':'Costa Rica',
        'CUB':'Cuba','CYP':'Cyprus','CZE':'Czechia','DEU':'Germany','DNK':'Denmark',
        'ECU':'Ecuador','ESP':'Spain','EST':'Estonia','FIN':'Finland','FRA':'France',
        'GBR':'UK','GEO':'Georgia','GHA':'Ghana','GRC':'Greece','GTM':'Guatemala',
        'HND':'Honduras','HRV':'Croatia','HUN':'Hungary','IDN':'Indonesia','IRL':'Ireland',
        'ISL':'Iceland','ITA':'Italy','JPN':'Japan','KAZ':'Kazakhstan','KEN':'Kenya',
        'KGZ':'Kyrgyzstan','KHM':'Cambodia','KOR':'South Korea','LAO':'Laos','LCA':'St. Lucia',
        'LSO':'Lesotho','LTU':'Lithuania','LUX':'Luxembourg','LVA':'Latvia','MAR':'Morocco',
        'MDV':'Maldives','MEX':'Mexico','MKD':'N. Macedonia','MLT':'Malta','MMR':'Myanmar',
        'MNE':'Montenegro','MNG':'Mongolia','MOZ':'Mozambique','MUS':'Mauritius','MYS':'Malaysia',
        'NAM':'Namibia','NGA':'Nigeria','NLD':'Netherlands','NOR':'Norway','NPL':'Nepal',
        'NZL':'New Zealand','PAK':'Pakistan','PER':'Peru','PHL':'Philippines','POL':'Poland',
        'PRT':'Portugal','PRY':'Paraguay','ROU':'Romania','RWA':'Rwanda','SEN':'Senegal',
        'SGP':'Singapore','SLV':'El Salvador','SRB':'Serbia','SVK':'Slovakia','SVN':'Slovenia',
        'SWE':'Sweden','SWZ':'Eswatini','TCD':'Chad','TLS':'Timor-Leste','TTO':'Trinidad',
        'TUN':'Tunisia','TUR':'Turkey','TZA':'Tanzania','UGA':'Uganda','URY':'Uruguay',
        'USA':'USA','UZB':'Uzbekistan','VNM':'Vietnam','ZAF':'S. Africa','ZMB':'Zambia',
        'BRN':'Brunei','KNA':'St. Kitts','GRD':'Grenada','VCT':'St. Vincent',
        'MDA':'Moldova','GMB':'Gambia',
    }

    y2024 = [(iso3_names[x['country']], x['value']) for x in data
             if x['year'] == 2024 and x['value'] is not None and x['country'] in iso3_names]
    y2024.sort(key=lambda x: -x[1])

    # Select diverse 42: top 30 + notable low-coverage
    selected = list(y2024[:30])
    low = [x for x in y2024 if x[1] < 30]
    for item in low[:12]:
        if item not in selected:
            selected.append(item)
    selected.sort(key=lambda x: -x[1])

    print(f"Countries: {len(selected)}")
    for n, v in selected:
        print(f"  {n}: {v}%")
    return selected, iso3_names, y2024


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart sorted by coverage (highest to lowest)
        - **Color**: By coverage tier — >80% teal, 50-80% amber, <50% orange-red
        - **Story**: Surprising leaders include Burkina Faso, Timor-Leste, Uzbekistan (all ≥99%),
          while Japan (17%) and Philippines (5%) lag far behind despite economic capacity.
          Bangladesh (90%) shows that income level does not determine vaccine uptake.
        """
    )
    return


@app.cell
def _(json, selected):
    chart_data = [{'n': n, 'v': round(v, 0)} for n, v in selected]
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data,


if __name__ == "__main__":
    app.run()
