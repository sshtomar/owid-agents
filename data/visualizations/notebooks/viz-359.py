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
        # Population Density Trends, 1990-2023 -- Methodology

        Sparkline grid showing population density (people per sq. km of land area)
        from 1990 to 2023 for the 24 most densely populated countries, excluding
        micro-territories. Each cell shows the trend line, start value, and end value.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-POP-DNST.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    EXCLUDE_TERMS = [
        'income','region','IDA','IBRD','World','dividend','OECD','Zone',
        'Europa','union','Union','countries','classification',
        'Eastern and Southern','Western and Central','North Africa',
        'Central Asia','Pacific','Latin America','Caribbean','Sub-Saharan',
        'Arab ','South Asia','East Asia','Europe & Central','North America',
        'Middle East','African Union'
    ]
    EXCLUDE_SMALL = [
        'Gibraltar','Bermuda','Macau','Monaco','San Marino','Liechtenstein',
        'Cayman','British Virgin','American Samoa','Guam','Aruba',
        'Channel Islands','Isle of Man','Faroe','French Polynesia',
        'New Caledonia','Sint Maarten','Curacao','Palau','Tuvalu',
        'Nauru','Maldives','Andorra'
    ]

    by_country = {}
    for p in data:
        n = p['countryName']
        if any(ex.lower() in n.lower() for ex in EXCLUDE_TERMS):
            continue
        if any(sm.lower() in n.lower() for sm in EXCLUDE_SMALL):
            continue
        if p['value'] is not None and p['year'] >= 1990:
            if n not in by_country:
                by_country[n] = {}
            by_country[n][p['year']] = p['value']

    result = []
    for n, ydata in by_country.items():
        if 1990 in ydata and 2023 in ydata:
            series = [round(ydata[y], 1) for y in range(1990, 2024) if y in ydata]
            result.append({'n': n, 's': series, 'e': round(ydata[1990], 1), 'l': round(ydata[2023], 1), 'y0': 1990})

    result.sort(key=lambda x: -x['l'])
    final = result[:24]
    print(f"Top 24 by 2023 density:")
    for r in final:
        pct = (r['l'] - r['e']) / r['e'] * 100
        print(f"  {r['n']}: {r['e']} -> {r['l']} ({pct:+.0f}%)")
    return final, result, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid (6 cols x 4 rows) normalized per country
        - **Sort**: By 2023 density (highest first), so denser countries are top-left
        - **Story**: Bahrain's density more than doubled (immigration-driven growth).
          Japan's density has slightly declined since 2011. Burundi's density surged +145%.
          Bangladesh remains one of the world's most densely populated large countries.
        """
    )
    return


@app.cell
def _(json, final):
    print(json.dumps(final, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
