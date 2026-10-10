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
        # Municipal Solid Waste Collection Coverage — Methodology

        Dataset: sdg--11-6-1--EN_REF_WASCOL (UN SDG 11.6.1)
        Indicator: % of urban population with access to municipal solid waste collection, 2018.
        Showing the 25 countries with the lowest coverage.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--11-6-1--EN_REF_WASCOL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_kws = ['World','Africa','Asia','Europe','America','Income','OECD','G20',
        'Oceania','Arab','Pacific','region','developing','Landlocked','Caribbean',
        'Micronesia','Melanesia','Polynesia','small states','small island','Northern','Southern',
        'Eastern','Western','Central','Sub-Saharan','Latin','Middle East']

    def is_country(name):
        return not any(kw.lower() in name.lower() for kw in exclude_kws)

    yr2018 = sorted(
        [d for d in data if d.get('year') == 2018 and d.get('value') is not None and is_country(d['countryName'])],
        key=lambda x: x['value']
    )
    print(f"Countries with 2018 data: {len(yr2018)}")
    print(f"Range: {yr2018[0]['value']:.1f}% - {yr2018[-1]['value']:.1f}%")
    return (yr2018,)


@app.cell
def _(json, yr2018):
    name_map = {
        'United Republic of Tanzania': 'Tanzania',
        "Lao People's Democratic Republic": 'Laos',
        'Democratic Republic of the Congo': 'DR Congo',
        'Republic of Moldova': 'Moldova',
        'Iran (Islamic Republic of)': 'Iran',
        'Bolivia (Plurinational State of)': 'Bolivia',
        'Venezuela (Bolivarian Republic of)': 'Venezuela',
        'Republic of Korea': 'South Korea',
        'Russian Federation': 'Russia',
        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
        'United States of America': 'United States',
        'Viet Nam': 'Vietnam',
    }
    bottom25 = [
        {"n": name_map.get(d["countryName"], d["countryName"]), "v": round(d["value"], 1)}
        for d in yr2018[:25]
    ]
    print(json.dumps(bottom25, separators=(",", ":")))
    return (bottom25,)


if __name__ == "__main__":
    app.run()
