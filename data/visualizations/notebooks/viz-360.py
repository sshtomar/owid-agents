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
        # Universal Health Coverage Service Index (SDG 3.8.1) -- Methodology

        Horizontal bar chart showing UHC service coverage index (0-100) for 40 countries,
        using each country's most recently available year. Index measures coverage of essential
        health services including reproductive, maternal, child and infectious disease services,
        service capacity, and access.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--UHC_INDEX_REPORTED.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    iso3_names = {
        'CAN':'Canada','NOR':'Norway','NZL':'New Zealand','AUS':'Australia','ISL':'Iceland',
        'GBR':'UK','SGP':'Singapore','KOR':'South Korea','CUB':'Cuba','FIN':'Finland',
        'BEL':'Belgium','CHE':'Switzerland','MCO':'Monaco','NLD':'Netherlands','CHN':'China',
        'JAM':'Jamaica','PLW':'Palau','TTO':'Trinidad','MUS':'Mauritius','GRC':'Greece',
        'EGY':'Egypt','ZAF':'S. Africa','AND':'Andorra','KGZ':'Kyrgyzstan','DOM':'Dominican Rep.',
        'CAF':'C. Afr. Rep.','AFG':'Afghanistan','TGO':'Togo','COG':'Congo','NER':'Niger',
        'MLI':'Mali','BEN':'Benin','MDG':'Madagascar','ETH':'Ethiopia','DJI':'Djibouti',
        'SOM':'Somalia','TCD':'Chad','PNG':'Papua NG','MRT':'Mauritania','MOZ':'Mozambique',
    }

    by_c = defaultdict(dict)
    for x in data:
        code = x['country']
        if x['value'] is not None and code in iso3_names:
            by_c[code][x['year']] = x['value']

    latest = {}
    for c, vals in by_c.items():
        last_yr = max(vals.keys())
        latest[c] = {'n': iso3_names[c], 'yr': last_yr, 'v': int(round(vals[last_yr]))}

    chart_data = sorted(latest.values(), key=lambda x: -x['v'])
    for item in chart_data:
        print(f"  {item['n']} ({item['yr']}): {item['v']}")
    return chart_data, by_c, iso3_names, latest


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart, sorted highest to lowest
        - **Color tiers**: >80 green, 60-80 teal, 40-60 amber, <40 red
        - **Story**: Canada leads at 92. China equals Switzerland at 85, Cuba reaches 86
          despite lower income. At the bottom, Chad (27) and Mozambique (23) reflect
          deep fragility in essential health service delivery.
        - **Year annotation**: Each bar shows the survey year since data is not available
          for all countries in the same year.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
