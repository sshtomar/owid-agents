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
        # Terrestrial Protected Areas: Conservation Gains — Methodology

        Slope chart comparing 2013 vs 2024 terrestrial protected area share (% of land).
        Data from World Bank indicator ER.LND.PTLD.ZS (Protected Planet).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-LND-PTLD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
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
        ('Bhutan','Bhutan'),('Cambodia','Cambodia'),('Germany','Germany'),
        ('Armenia','Armenia'),('Cyprus','Cyprus'),('Croatia','Croatia'),
        ('Brazil','Brazil'),('Japan','Japan'),('France','France'),
        ('Australia','Australia'),('China','China'),('Kenya','Kenya'),
        ('Canada','Canada'),('India','India'),
    ]

    chart_data = []
    for country_key, short_name in selected:
        if country_key not in by_country:
            continue
        vals = by_country[country_key]
        a = vals.get(2013)
        b = vals.get(2024, vals.get(2023, vals.get(2022)))
        if a is not None and b is not None:
            chart_data.append({'n': short_name, 'a': round(a, 1), 'b': round(b, 1)})
            print(f"{short_name}: {a:.1f}% -> {b:.1f}% (+{b-a:.1f}pp)")

    print("\nFinal JSON:")
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, by_country, filtered, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — shows change between two specific years
        - **Country selection**: Mix of high-changers, high-total, and laggards
        - **Reference line**: 30% at the UN CBD "30x30" target (protect 30% by 2030)
        - **Highlights**:
            - Bhutan leads at 51.6% (long-standing conservation constitution)
            - Croatia: 13.8% → 38.4% (EU accession-driven conservation expansion)
            - Cambodia: 26.3% → 39.8% (ASEAN biodiversity commitments)
            - China and Kenya show little change despite large land areas
        - **Color**: by percentage point change (warm = largest gains)
        """
    )
    return


if __name__ == "__main__":
    app.run()
