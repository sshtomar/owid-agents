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
        # The Sanitation Leap: Safely Managed Sanitation Services, 2000 vs 2024 -- Methodology

        Slope chart comparing the share of population using safely managed
        sanitation services between ~2000 and ~2024 for countries spanning
        the full range of access levels.
        Source: WHO/UNICEF JMP (WSH_SANITATION_SAFELY_MANAGED).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WSH_SANITATION_SAFELY_MANAGED.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} rows")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict

    iso_names = {
        'AFG': 'Afghanistan', 'AGO': 'Angola', 'BGD': 'Bangladesh',
        'BRA': 'Brazil', 'CMR': 'Cameroon', 'CHN': 'China',
        'COD': 'DR Congo', 'EGY': 'Egypt', 'ETH': 'Ethiopia',
        'FRA': 'France', 'DEU': 'Germany', 'GHA': 'Ghana',
        'IND': 'India', 'IDN': 'Indonesia', 'IRN': 'Iran',
        'IRQ': 'Iraq', 'ITA': 'Italy', 'JPN': 'Japan',
        'JOR': 'Jordan', 'KEN': 'Kenya', 'KOR': 'South Korea',
        'MDG': 'Madagascar', 'MEX': 'Mexico', 'MAR': 'Morocco',
        'MOZ': 'Mozambique', 'NGA': 'Nigeria', 'PAK': 'Pakistan',
        'PER': 'Peru', 'PHL': 'Philippines', 'RUS': 'Russia',
        'RWA': 'Rwanda', 'SEN': 'Senegal', 'SLE': 'Sierra Leone',
        'ZAF': 'South Africa', 'ESP': 'Spain', 'SDN': 'Sudan',
        'SWE': 'Sweden', 'TZA': 'Tanzania', 'THA': 'Thailand',
        'TUN': 'Tunisia', 'TUR': 'Turkey', 'UGA': 'Uganda',
        'GBR': 'United Kingdom', 'VNM': 'Vietnam', 'YEM': 'Yemen',
        'ZMB': 'Zambia', 'ZWE': 'Zimbabwe', 'PRY': 'Paraguay',
        'KGZ': 'Kyrgyzstan', 'CHL': 'Chile', 'BOL': 'Bolivia',
        'NER': 'Niger', 'SGP': 'Singapore', 'KWT': 'Kuwait',
        'MLI': 'Mali', 'BEN': 'Benin', 'TCD': 'Chad',
        'HTI': 'Haiti', 'NIC': 'Nicaragua', 'GTM': 'Guatemala',
        'ECU': 'Ecuador', 'DZA': 'Algeria', 'LBN': 'Lebanon',
        'BLR': 'Belarus', 'ARM': 'Armenia'
    }

    by_ctry = defaultdict(dict)
    for r in data:
        if r['value'] is not None:
            by_ctry[r['country']][r['year']] = r['value']

    slope = []
    for code, name in iso_names.items():
        if code in by_ctry:
            early = [(y, v) for y, v in by_ctry[code].items() if 2000 <= y <= 2005]
            late = [(y, v) for y, v in by_ctry[code].items() if 2019 <= y <= 2024]
            if early and late:
                a_yr, a_v = min(early, key=lambda x: x[0])
                b_yr, b_v = max(late, key=lambda x: x[0])
                slope.append({'n': name, 'a': round(a_v, 1), 'b': round(b_v, 1)})

    slope.sort(key=lambda x: x['b'])
    print(f"Countries: {len(slope)}")
    for s in slope:
        diff = s['b'] - s['a']
        print(f"  {s['n']}: {s['a']:.1f} -> {s['b']:.1f} ({diff:+.1f})")
    return slope, by_ctry, iso_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points (~2000 vs ~2024)
        - **Countries**: 40 spanning the full access range, from <10% to 100%
        - **Highlights**: India's extraordinary improvement (+59pp); Jordan, Mexico, Tanzania;
          some countries regressed (DR Congo, Belarus, Yemen)
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
