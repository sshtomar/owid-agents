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
        # Hepatitis C Prevalence by Country, 2015 -- Methodology

        Horizontal bar chart showing the percentage of the general population with
        chronic hepatitis C infection. Reveals geographic concentration of the burden.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--HEPATITIS_HCV_PREVALENCE_PER100.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    iso_names = {
        'GAB': 'Gabon', 'PAK': 'Pakistan', 'BDI': 'Burundi', 'ARM': 'Armenia',
        'KAZ': 'Kazakhstan', 'BWA': 'Botswana', 'LSO': 'Lesotho', 'SWZ': 'Eswatini',
        'ZAF': 'South Africa', 'MDA': 'Moldova', 'GHA': 'Ghana', 'BFA': 'Burkina Faso',
        'QAT': 'Qatar', 'KHM': 'Cambodia', 'PNG': 'Papua New Guinea', 'BEN': 'Benin',
        'BLR': 'Belarus', 'GEO': 'Georgia', 'EGY': 'Egypt', 'LBY': 'Libya',
        'VNM': 'Vietnam', 'CMR': 'Cameroon', 'GIN': 'Guinea', 'TJK': 'Tajikistan',
        'MNG': 'Mongolia'
    }
    exclude_regions = {'AFR', 'AMR', 'EMR', 'EUR', 'SEAR', 'WPR', 'Global'}

    by_country = {}
    for p in data:
        if p['countryName'] not in exclude_regions and p['year'] == 2015 and p['value'] is not None:
            name = iso_names.get(p['countryName'], p['countryName'])
            by_country[name] = p['value']

    result = [{'n': k, 'v': round(v, 2)} for k, v in by_country.items()]
    result.sort(key=lambda x: -x['v'])
    result = result[:25]

    print(f"Top 25 countries by HCV prevalence:")
    for r in result:
        print(f"  {r['n']}: {r['v']}%")
    return result, by_country, iso_names, exclude_regions


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart for country ranking comparison
        - **Color**: Warm ramp from orange (≥4%) through amber/yellow/green (<1%)
        - **Story**: Gabon (5.46%) and Pakistan (5.45%) lead globally. The burden is
          concentrated in sub-Saharan Africa and Central Asia. Pakistan's high rate
          reflects historical unsafe injection practices and poor blood safety.
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
