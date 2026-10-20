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
        # The Diabetes Rise: Raised Blood Glucose, 1980 vs 2014 -- Methodology

        Slope chart comparing the prevalence of raised fasting blood glucose
        (crude estimate, % of adults) between 1980 and 2014.
        Highlights the dramatic rise in Pacific island nations and the Middle East.
        Source: WHO Global Health Observatory (NCD_GLUC_03).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_GLUC_03.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} rows")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict

    iso_names = {
        'AFG': 'Afghanistan', 'DZA': 'Algeria', 'ARG': 'Argentina',
        'AUS': 'Australia', 'BHR': 'Bahrain', 'BGD': 'Bangladesh',
        'BLZ': 'Belize', 'BRA': 'Brazil', 'CHN': 'China',
        'COG': 'Congo', 'CRI': 'Costa Rica', 'HRV': 'Croatia',
        'CUB': 'Cuba', 'EGY': 'Egypt', 'FIN': 'Finland',
        'FRA': 'France', 'DEU': 'Germany', 'GHA': 'Ghana',
        'HUN': 'Hungary', 'IND': 'India', 'IDN': 'Indonesia',
        'IRN': 'Iran', 'IRQ': 'Iraq', 'IRL': 'Ireland',
        'ITA': 'Italy', 'JPN': 'Japan', 'JOR': 'Jordan',
        'KEN': 'Kenya', 'KWT': 'Kuwait', 'MYS': 'Malaysia',
        'MDV': 'Maldives', 'MEX': 'Mexico', 'MAR': 'Morocco',
        'MOZ': 'Mozambique', 'NGA': 'Nigeria', 'NOR': 'Norway',
        'OMN': 'Oman', 'PAK': 'Pakistan', 'PNG': 'Papua New Guinea',
        'PRY': 'Paraguay', 'POL': 'Poland', 'PRT': 'Portugal',
        'QAT': 'Qatar', 'RUS': 'Russia', 'SAU': 'Saudi Arabia',
        'ZAF': 'South Africa', 'ESP': 'Spain', 'LKA': 'Sri Lanka',
        'SDN': 'Sudan', 'SUR': 'Suriname', 'SWE': 'Sweden',
        'SYR': 'Syria', 'THA': 'Thailand', 'TTO': 'Trinidad',
        'TUN': 'Tunisia', 'TUR': 'Turkey', 'UGA': 'Uganda',
        'ARE': 'UAE', 'GBR': 'United Kingdom', 'USA': 'United States',
        'VEN': 'Venezuela', 'VNM': 'Vietnam', 'YEM': 'Yemen',
        'NRU': 'Nauru', 'MHL': 'Marshall Islands', 'PLW': 'Palau',
        'TON': 'Tonga', 'VUT': 'Vanuatu', 'WSM': 'Samoa',
        'KIR': 'Kiribati', 'TUV': 'Tuvalu', 'FSM': 'Micronesia',
        'BHS': 'Bahamas'
    }

    by_ctry = defaultdict(dict)
    for r in data:
        if r['value'] is not None:
            by_ctry[r['country']][r['year']] = r['value']

    slope = []
    for code, yrs in by_ctry.items():
        early = [(y, v) for y, v in yrs.items() if 1980 <= y <= 1985]
        late = [(y, v) for y, v in yrs.items() if 2010 <= y <= 2014]
        if early and late:
            a_yr, a_v = min(early, key=lambda x: x[0])
            b_yr, b_v = max(late, key=lambda x: x[0])
            name = iso_names.get(code, code)
            slope.append({'n': name, 'a': round(a_v, 1), 'b': round(b_v, 1)})

    # Take top 20 by 2014 value (highest burden)
    slope.sort(key=lambda x: -x['b'])
    chart_data = slope[:20]
    print(f"Selected {len(chart_data)} countries")
    for s in chart_data:
        print(f"  {s['n']}: {s['a']:.1f} -> {s['b']:.1f}")
    return chart_data, slope, by_ctry, iso_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points (1980 vs ~2014) across 20 countries
        - **Countries**: Top 20 highest prevalence in 2014; dominated by Pacific islands
        - **Highlights**: Nauru, Cook Islands, Marshall Islands saw explosive rises;
          Middle Eastern countries like Egypt and Qatar also jumped sharply
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
