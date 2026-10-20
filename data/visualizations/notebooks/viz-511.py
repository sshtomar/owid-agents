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
        # Health Expenditure as % of GDP -- Methodology

        This notebook documents the data pipeline for the chart comparing
        current health expenditure as a share of GDP across major economies.
        Source: WHO Global Health Expenditure Database (GHED), indicator GHED_CHEGDP_SHA2011.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--GHED_CHEGDP_SHA2011.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    # Country name mapping (ISO 3-letter -> readable)
    iso_names = {
        'USA': 'United States', 'JPN': 'Japan', 'AUT': 'Austria',
        'FRA': 'France', 'DEU': 'Germany', 'PRT': 'Portugal',
        'GBR': 'United Kingdom', 'NLD': 'Netherlands', 'CHL': 'Chile',
        'FIN': 'Finland', 'NOR': 'Norway', 'GRC': 'Greece',
        'ZAF': 'South Africa', 'KOR': 'South Korea', 'RUS': 'Russia',
        'MEX': 'Mexico', 'MAR': 'Morocco', 'CHN': 'China',
        'THA': 'Thailand', 'VNM': 'Vietnam', 'EGY': 'Egypt',
        'TZA': 'Tanzania', 'IDN': 'Indonesia', 'NGA': 'Nigeria',
        'PAK': 'Pakistan', 'ETH': 'Ethiopia',
    }

    by_ctry = defaultdict(dict)
    for r in data:
        if r['value'] is not None:
            by_ctry[r['country']][r['year']] = r['value']

    bar_data = []
    for code, name in iso_names.items():
        if code in by_ctry:
            recent = [(y, v) for y, v in by_ctry[code].items() if 2016 <= y <= 2023]
            if recent:
                best_y, best_v = max(recent, key=lambda x: x[0])
                bar_data.append({'n': name, 'v': round(best_v, 1), 'y': best_y})

    bar_data.sort(key=lambda x: -x['v'])
    print(f"Countries selected: {len(bar_data)}")
    for b in bar_data:
        print(f"  {b['n']} ({b['y']}): {b['v']:.1f}%")
    return bar_data, by_ctry, iso_names


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — best for ranking many countries at a single time point
        - **Country selection**: 26 countries spanning all income groups and regions
        - **Year**: Most recent available (2016-2023 range)
        - **Highlights**: USA outlier at 17.4%; developing countries mostly 3-5%
        """
    )
    return


@app.cell
def _(json, bar_data):
    print(json.dumps(bar_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
