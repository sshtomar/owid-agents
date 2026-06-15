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
        # Tuberculosis Treatment Coverage — Methodology

        Horizontal bar chart showing TB treatment coverage (2023) for 44 countries.
        WHO data; covers the share of estimated new and relapse TB cases that received
        treatment. Mongolia is a notable outlier at 19%.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--TB_1.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso_to_name = {
        'MNG':'Mongolia','GHA':'Ghana','SLB':'Solomon Islands','KIR':'Kiribati',
        'MNE':'Montenegro','SYR':'Syria','MUS':'Mauritius','MAC':'Macao SAR, China',
        'CMR':'Cameroon','IRQ':'Iraq','MDG':'Madagascar','GEO':'Georgia',
        'OMN':'Oman','PSE':'Palestine','VUT':'Vanuatu','BIH':'Bosnia & Herzegovina',
        'GMB':'Gambia','ETH':'Ethiopia','YEM':'Yemen',
        'PRI':'Puerto Rico','MYS':'Malaysia','GIN':'Guinea','ZAF':'South Africa',
        'PHL':'Philippines','CZE':'Czechia','SVN':'Slovenia','GTM':'Guatemala',
        'ATG':'Antigua & Barbuda','VCT':'St. Vincent & Grenadines',
        'MLT':'Malta','GRD':'Grenada','TUV':'Tuvalu','SYC':'Seychelles',
        'DMA':'Dominica','RWA':'Rwanda','KOR':'South Korea','KAZ':'Kazakhstan',
        'UZB':'Uzbekistan','ARM':'Armenia','IRL':'Ireland','MDA':'Moldova',
        'FSM':'Micronesia','NRU':'Nauru','WSM':'Samoa','LBN':'Lebanon',
        'CPV':'Cabo Verde','COK':'Cook Islands','NIU':'Niue','TON':'Tonga',
        'MHL':'Marshall Islands','PLW':'Palau','FRA':'France','SWE':'Sweden',
        'ESP':'Spain','PRT':'Portugal','NOR':'Norway','SGP':'Singapore',
        'GBR':'United Kingdom','SAU':'Saudi Arabia','NLD':'Netherlands'
    }
    exclude = {'GLOBAL','WB_LMI','WB_HIC','WB_LIC','WB_MIC','WB_LMIC','WB_UMIC',
               'EUR','AMR','AFR','EMR','SEAR','WPR','G7','BRICS','OECD'}

    pts = {}
    for p in data:
        if p['value'] is None:
            continue
        pts.setdefault(p['country'], {})[p['year']] = p['value']

    pts_2023 = []
    for cn, yrs in pts.items():
        if 2023 not in yrs or yrs[2023] > 100 or cn in exclude:
            continue
        name = iso_to_name.get(cn)
        if name is None:
            continue
        pts_2023.append((name, yrs[2023]))

    pts_2023.sort(key=lambda x: x[1])
    print(f"Countries with 2023 coverage: {len(pts_2023)}")
    for n, v in pts_2023[:5]:
        print(f"  {n}: {v:.0f}%")
    return exclude, iso_to_name, pts, pts_2023


@app.cell
def _(pts_2023):
    chart_data = [{"n": n, "v": int(v)} for n, v in pts_2023]
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — best for ranked categorical comparison
        - **Country selection**: All countries with WHO 2023 data + resolvable ISO name (44 total)
        - **Year**: 2023 (most recent)
        - **Color**: Diverging green-to-red scale by coverage level
        - **Highlights**: Mongolia 19%; seven countries at 100%
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
