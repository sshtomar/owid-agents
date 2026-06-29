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
        # Armed Forces as % of Labor Force: 1990 vs 2020 — Methodology

        Slope chart showing military personnel share of labor force change over 30 years.
        Data from World Bank indicator MS.MIL.TOTL.TF.ZS (IISS).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--MS-MIL-TOTL-TF-ZS.json"
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

    selected = [
        ("Iraq", "Iraq"), ("Jordan", "Jordan"), ("Israel", "Israel"),
        ("Korea, Dem. People's Rep.", "N. Korea"), ("Cuba", "Cuba"),
        ("Greece", "Greece"), ("Korea, Rep.", "S. Korea"),
        ("Iran, Islamic Rep.", "Iran"), ("Egypt, Arab Rep.", "Egypt"),
        ("Belgium", "Belgium"), ("Hungary", "Hungary"), ("Algeria", "Algeria"),
        ("Germany", "Germany"), ("China", "China"), ("Brazil", "Brazil"),
        ("India", "India"), ("Japan", "Japan"),
    ]

    chart_data = []
    for country_key, short_name in selected:
        if country_key not in by_country:
            continue
        vals = by_country[country_key]
        a = vals.get(1990)
        b = vals.get(2020, vals.get(2019, vals.get(2018)))
        if a is not None and b is not None:
            chart_data.append({'n': short_name, 'a': round(a, 2), 'b': round(b, 2)})
            print(f"{short_name}: {a:.2f}% -> {b:.2f}% ({b-a:+.2f}pp)")

    print("\nFinal JSON:")
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, by_country, filtered, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows change between two specific years (1990 vs 2020)
        - **Country selection**: 17 countries from very high military (Iraq 1990) to very low (Japan)
        - **Highlights**:
            - Iraq: 33.98% in 1990 (Gulf War era, conscript army) → 4.4% in 2020 (post-2003 restructuring)
            - Jordan: 12.75% → 3.98% (partial demobilization)
            - North Korea remains the outlier at ~8.6% (world's highest per-capita military)
            - NATO European countries (Belgium, Germany, Hungary) drastically reduced military burden post-Cold War
            - Algeria increased slightly as it expanded its military capacity in the Sahel context
        - **Color**: by direction and magnitude of change (warm = large decrease, green = increase)
        """
    )
    return


if __name__ == "__main__":
    app.run()
