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
        # Food Waste per Capita — Methodology

        Dataset: sdg--12-3-1--AG_FOOD_WST_PC (UN SDG 12.3.1)
        Indicator: Food waste at retail and consumer level, kg per person per year (2022)
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--12-3-1--AG_FOOD_WST_PC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    # Filter to 2022 country data
    exclude_kws = ['World','Africa','Asia','Europe','America','Income','OECD','G20',
        'Oceania','Arab','Pacific','region','developing','Landlocked','Caribbean',
        'Micronesia','Melanesia','Polynesia','small states','small island']
    tiny_islands = {'Maldives','Seychelles','Vanuatu','Tonga','Samoa','Kiribati',
                   'Palau','Marshall Islands','Tuvalu','Nauru','Cook Islands',
                   'Micronesia (Federated States of)','Saint Barthélemy',
                   'Wallis and Futuna Islands','Western Sahara','Mayotte',
                   'Guadeloupe','Martinique','Réunion','French Guiana',
                   'Sint Maarten (Dutch part)','French Polynesia','New Caledonia'}

    def is_country(name):
        if name in tiny_islands:
            return False
        return not any(kw.lower() in name.lower() for kw in exclude_kws)

    yr2022 = [d for d in data if d.get('year') == 2022 and d.get('value') is not None and is_country(d['countryName'])]
    yr2022_sorted = sorted(yr2022, key=lambda x: -x['value'])
    print(f"Countries with 2022 data: {len(yr2022_sorted)}")
    print(f"Range: {yr2022_sorted[-1]['value']:.1f} - {yr2022_sorted[0]['value']:.1f} kg")
    return is_country, yr2022, yr2022_sorted


@app.cell
def _(yr2022_sorted):
    # Top 20 countries
    name_map = {
        'United Republic of Tanzania': 'Tanzania',
        "Lao People's Democratic Republic": 'Laos',
        'Democratic Republic of the Congo': 'DR Congo',
        'Republic of Moldova': 'Moldova',
        'Iran (Islamic Republic of)': 'Iran',
    }
    top20 = [
        {"n": name_map.get(d["countryName"], d["countryName"]), "v": round(d["value"], 1)}
        for d in yr2022_sorted[:20]
    ]
    print(f"Top 20: {top20[:3]} ...")
    return (top20,)


@app.cell
def _(json, top20):
    print(json.dumps(top20, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
