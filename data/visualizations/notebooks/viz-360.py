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
        # Mean Total Cholesterol by Country, ~2011 — Methodology

        This notebook documents the data pipeline behind viz-360.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NCD_CHOL_MEANTOTALCHOL_A.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    # Filter to 2011 (best single-year coverage: 37 countries, but some have 2 entries per country due to sex-disaggregated source)
    # Average duplicates per country
    by_country = defaultdict(list)
    for p in data:
        if p["year"] == 2011 and p["value"] is not None and len(p["country"]) == 3:
            by_country[p["country"]].append(p["value"])
    averaged = {c: round(sum(vs)/len(vs), 2) for c, vs in by_country.items()}
    print(f"Countries in 2011: {len(averaged)}")
    sorted_countries = sorted(averaged.items(), key=lambda x: x[1], reverse=True)
    print("Top 5:", sorted_countries[:5])
    print("Bottom 5:", sorted_countries[-5:])
    return averaged, by_country, sorted_countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — ranks all countries in a single year
        - **Year selected**: 2011 (highest per-year country count: 37 countries)
        - **Duplicates**: The WHO dataset occasionally stores male and female estimates separately; these are averaged to get a single per-country figure
        - **WHO guideline**: 5.0 mmol/L is the threshold for raised total cholesterol
        - **Story**: Central European countries cluster above the threshold; West African nations are well below
        """
    )
    return


@app.cell
def _(json, sorted_countries):
    cmap = {
        'AUT': 'Austria', 'ARM': 'Armenia', 'AZE': 'Azerbaijan', 'BEN': 'Benin',
        'BOL': 'Bolivia', 'BRA': 'Brazil', 'BRN': 'Brunei', 'CIV': "Cote d'Ivoire",
        'CZE': 'Czech Rep.', 'DEU': 'Germany', 'DOM': 'Dom. Republic',
        'GHA': 'Ghana', 'GMB': 'Gambia', 'GNQ': 'Eq. Guinea', 'GTM': 'Guatemala',
        'IDN': 'Indonesia', 'JOR': 'Jordan', 'KGZ': 'Kyrgyzstan',
        'LBR': 'Liberia', 'LSO': 'Lesotho', 'MAR': 'Morocco',
        'MDA': 'Moldova', 'MHL': 'Marshall Is.', 'MNE': 'Montenegro',
        'NIC': 'Nicaragua', 'NRU': 'Nauru', 'OMN': 'Oman', 'PAN': 'Panama',
        'PRY': 'Paraguay', 'QAT': 'Qatar', 'SGP': 'Singapore',
        'SLE': 'Sierra Leone', 'SLB': 'Solomon Is.', 'SVN': 'Slovenia',
        'SOM': 'Somalia', 'SUR': 'Suriname', 'TGO': 'Togo', 'THA': 'Thailand',
        'TUV': 'Tuvalu', 'UGA': 'Uganda', 'URY': 'Uruguay', 'UZB': 'Uzbekistan',
        'VCT': 'St Vincent', 'ZMB': 'Zambia', 'ATG': 'Antigua', 'GEO': 'Georgia',
        'SYC': 'Seychelles', 'BLZ': 'Belize',
    }
    chart_data = [{"n": cmap.get(c, c), "v": v} for c, v in sorted_countries]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
