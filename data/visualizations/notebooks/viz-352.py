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
        # Physical Inactivity Rates by Country -- Methodology

        Slope chart comparing earliest available survey year to most recent available
        year for each country. Data from WHO GHO indicator NCD_PAA (age-standardized
        prevalence of insufficient physical activity among adults 18+).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_PAA.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    iso3_names = {
        'USA': 'United States', 'GBR': 'United Kingdom', 'DEU': 'Germany',
        'JPN': 'Japan', 'CHN': 'China', 'IND': 'India',
        'BRA': 'Brazil', 'ZAF': 'South Africa', 'AUS': 'Australia',
        'NGA': 'Nigeria', 'SAU': 'Saudi Arabia', 'MEX': 'Mexico',
        'CAN': 'Canada', 'KOR': 'South Korea', 'PHL': 'Philippines',
        'PAK': 'Pakistan', 'ARG': 'Argentina', 'TUR': 'Turkey',
        'NOR': 'Norway', 'SWE': 'Sweden', 'ETH': 'Ethiopia',
        'KWT': 'Kuwait', 'QAT': 'Qatar', 'ARE': 'UAE',
        'THA': 'Thailand', 'COL': 'Colombia', 'KEN': 'Kenya',
        'MOZ': 'Mozambique', 'RUS': 'Russia', 'ESP': 'Spain',
        'ITA': 'Italy', 'PRT': 'Portugal', 'DEU': 'Germany',
        'GHA': 'Ghana', 'IND': 'India',
    }
    selected_names = {'UAE', 'Saudi Arabia', 'Kuwait', 'Qatar', 'South Korea', 'Japan',
        'India', 'Portugal', 'Turkey', 'Italy', 'Philippines', 'South Africa',
        'United States', 'Canada', 'Brazil', 'Pakistan', 'Thailand', 'Colombia',
        'Australia', 'Spain', 'United Kingdom', 'China', 'Nigeria', 'Russia',
        'Sweden', 'Ethiopia', 'Germany', 'Mozambique', 'Kenya'}
    by_country = defaultdict(list)
    for p in data:
        name = iso3_names.get(p['country'])
        if name in selected_names and p['value'] is not None:
            by_country[name].append((p['year'], p['value']))
    rows = []
    for name, pts in sorted(by_country.items()):
        pts_s = sorted(pts)
        if len(pts_s) >= 2:
            rows.append({'n': name, 'a': round(pts_s[0][1], 1), 'b': round(pts_s[-1][1], 1)})
    rows.sort(key=lambda x: -x['b'])
    print(f"Rows for chart: {len(rows)}")
    return by_country, iso3_names, rows, selected_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- shows direction and magnitude of change between
          first and latest available survey for each country
        - **Country selection**: 29 diverse countries representing all world regions
        - **Color**: warm (orange/red) if inactivity increased, cool (green/teal) if decreased
        - **Story**: Gulf states lead in sedentariness (60%+); South Korea, Japan, India
          are rising sharply; Germany, Sweden, Spain improved; Sub-Saharan Africa
          remains most physically active despite growing wealth
        """
    )
    return


@app.cell
def _(json, rows):
    print(json.dumps(rows, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
