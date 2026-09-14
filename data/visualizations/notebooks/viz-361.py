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
        # Healthy Life Expectancy (HALE) at Age 60 — Methodology

        Horizontal bar chart showing how many more years of healthy life a 60-year-old
        can expect in different countries. The global range spans from ~8 to ~20 years.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHOSIS_000007.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    ISO3_NAMES = {
        'AFG': 'Afghanistan', 'AGO': 'Angola', 'ALB': 'Albania', 'ARE': 'UAE',
        'ARM': 'Armenia', 'AUS': 'Australia', 'AUT': 'Austria',
        'BGD': 'Bangladesh', 'BGR': 'Bulgaria', 'BFA': 'Burkina Faso',
        'BRA': 'Brazil', 'BWA': 'Botswana', 'CAF': 'Central African Rep.',
        'CAN': 'Canada', 'CHE': 'Switzerland', 'CHL': 'Chile', 'CHN': 'China',
        'COD': 'Congo (DRC)', 'COG': 'Congo (Rep.)', 'COL': 'Colombia',
        'CRI': 'Costa Rica', 'CUB': 'Cuba', 'DEU': 'Germany', 'DJI': 'Djibouti',
        'DNK': 'Denmark', 'DOM': 'Dominican Rep.', 'ECU': 'Ecuador', 'EGY': 'Egypt',
        'ESP': 'Spain', 'ETH': 'Ethiopia', 'FIN': 'Finland', 'FJI': 'Fiji',
        'FRA': 'France', 'GAB': 'Gabon', 'GBR': 'United Kingdom', 'GHA': 'Ghana',
        'GNB': 'Guinea-Bissau', 'GRC': 'Greece', 'GTM': 'Guatemala',
        'HND': 'Honduras', 'HUN': 'Hungary', 'IDN': 'Indonesia', 'IND': 'India',
        'IRL': 'Ireland', 'IRN': 'Iran', 'ISL': 'Iceland', 'ISR': 'Israel',
        'ITA': 'Italy', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya',
        'KGZ': 'Kyrgyzstan', 'KIR': 'Kiribati', 'KOR': 'South Korea',
        'KWT': 'Kuwait', 'LCA': 'Saint Lucia', 'LSO': 'Lesotho',
        'MAR': 'Morocco', 'MDG': 'Madagascar', 'MEX': 'Mexico', 'MKD': 'N. Macedonia',
        'MOZ': 'Mozambique', 'MWI': 'Malawi', 'NAM': 'Namibia', 'NER': 'Niger',
        'NGA': 'Nigeria', 'NIC': 'Nicaragua', 'NLD': 'Netherlands',
        'NOR': 'Norway', 'NZL': 'New Zealand', 'PAK': 'Pakistan', 'PAN': 'Panama',
        'PER': 'Peru', 'PHL': 'Philippines', 'PRT': 'Portugal', 'QAT': 'Qatar',
        'RUS': 'Russia', 'SAU': 'Saudi Arabia', 'SDN': 'Sudan', 'SEN': 'Senegal',
        'SGP': 'Singapore', 'SLB': 'Solomon Islands', 'SLE': 'Sierra Leone',
        'SOM': 'Somalia', 'SSD': 'South Sudan', 'SWE': 'Sweden', 'SWZ': 'Eswatini',
        'TCD': 'Chad', 'THA': 'Thailand', 'TUR': 'Türkiye', 'TZA': 'Tanzania',
        'UGA': 'Uganda', 'USA': 'United States', 'VEN': 'Venezuela',
        'VNM': 'Vietnam', 'ZAF': 'South Africa', 'ZMB': 'Zambia',
    }

    by_country = defaultdict(list)
    for row in data:
        cc = row['country']
        if '_' in cc or cc in {'AFR','AMR','EMR','EUR','SEAR','WPR','GLOBAL'}:
            continue
        if cc in ISO3_NAMES and row['value'] is not None:
            by_country[cc].append(row)

    latest = {}
    for cc, rows in by_country.items():
        rows.sort(key=lambda r: r['year'])
        latest[cc] = {'n': ISO3_NAMES[cc], 'v': round(rows[-1]['value'], 1), 'y': rows[-1]['year']}

    sorted_vals = sorted(latest.values(), key=lambda x: -x['v'])
    chart_data = sorted_vals[:15] + sorted_vals[-15:]
    seen = set()
    dedup = []
    for r in chart_data:
        if r['n'] not in seen:
            seen.add(r['n'])
            dedup.append(r)
    dedup.sort(key=lambda x: -x['v'])
    print(f"Countries: {len(dedup)}")
    for r in dedup:
        print(f"  {r['n']}: {r['v']} yrs ({r['y']})")
    return dedup


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — clear comparison of a single health metric
        - **Country selection**: Top 15 and bottom 15, showing the full global range
        - **Key story**: Spain has 20.3 healthy years after 60; Central African Republic has 8.3 — a 2.5x difference
        - **Color**: Warm (low HALE) to cool (high HALE)
        """
    )
    return


@app.cell
def _(dedup, json):
    print(json.dumps(dedup, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
