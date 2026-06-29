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
        # Risk of Catastrophic Surgical Expenditure — Methodology

        Horizontal bar chart showing % of population at financial risk if they need surgery.
        Data from World Bank indicator SH.SGR.CRSK.ZS (WHO).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-SGR-CRSK-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points, year range: "
          f"{min(d['year'] for d in data)}-{max(d['year'] for d in data)}")
    return data, raw


@app.cell
def _(data, json):
    from collections import defaultdict

    EXCLUDE_CODES = {
        'ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','XC','XD','XE','XF','XG','XH',
        'XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU','B8','F1','OE',
        'S1','S2','S3','S4','T2','T3','T4','T5','T6','T7','V1','V2','V3','V4',
        'Z4','Z7','EU','1A','1W','4E','7E','8S'
    }

    filtered = [d for d in data if d['country'].isalpha() and len(d['country']) == 2
                and d['country'] not in EXCLUDE_CODES and d['value'] is not None]

    by_country = defaultdict(dict)
    for d in filtered:
        by_country[d['countryName']][d['year']] = d['value']

    name_map = {"Cote d'Ivoire": "Côte d'Ivoire", "Congo, Dem. Rep.": "DR Congo",
                "Iran, Islamic Rep.": "Iran", "Korea, Rep.": "South Korea"}
    selected_keys = [
        "Cote d'Ivoire", "Burundi", "Congo, Dem. Rep.", "Chad",
        "Cameroon", "Angola", "Bangladesh", "Iran, Islamic Rep.",
        "Brazil", "India", "Indonesia", "Colombia", "China",
        "Italy", "Japan", "Korea, Rep.", "France", "Germany", "Finland"
    ]

    chart_data = []
    for k in selected_keys:
        if k not in by_country:
            continue
        vals = by_country[k]
        max_year = max(y for y in vals if y >= 2015)
        if max_year:
            chart_data.append({
                'n': name_map.get(k, k),
                'v': round(vals[max_year], 1),
                'y': max_year
            })
            print(f"{name_map.get(k, k)}: {vals[max_year]:.1f}% ({max_year})")

    print("\nFinal JSON:")
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, by_country, filtered, name_map, selected_keys


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — ranked comparison of a single metric across countries
        - **Country selection**: 19 countries spanning full range (0% to 100%)
        - **Highlights**:
            - In Côte d'Ivoire and Burundi, ~100% of the population faces catastrophic expenditure risk for surgery
            - Universal health coverage in Germany, Finland, France: essentially 0%
            - China at 3.7% reflects rapid expansion of its national health insurance system
            - India at 20.4% reflects out-of-pocket burden despite Ayushman Bharat scheme
        - **Color**: by risk level (deep terra = highest risk, green = lowest)
        """
    )
    return


if __name__ == "__main__":
    app.run()
