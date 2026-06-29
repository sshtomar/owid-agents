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
        # International Tourism: COVID-19 Collapse — Methodology

        Slope chart comparing 2019 vs 2020 tourist arrivals (millions) for top destinations.
        Data from World Bank indicator ST.INT.ARVL (UN World Tourism Organization).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
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
        ('France','France'),('China','China'),('Italy','Italy'),
        ('Hungary','Hungary'),('Croatia','Croatia'),
        ('Hong Kong SAR, China','Hong Kong'),('Germany','Germany'),
        ('Greece','Greece'),('Austria','Austria'),('Japan','Japan'),
        ('Korea, Rep.','South Korea'),('Indonesia','Indonesia'),
    ]

    chart_data = []
    for country_key, short_name in selected:
        if country_key not in by_country:
            continue
        vals = by_country[country_key]
        v2019 = vals.get(2019)
        v2020 = vals.get(2020)
        if v2019 and v2020:
            pct = (v2019 - v2020) / v2019 * 100
            chart_data.append({'n': short_name, 'a': round(v2019/1e6, 1), 'b': round(v2020/1e6, 1)})
            print(f"{short_name}: {v2019/1e6:.1f}M -> {v2020/1e6:.1f}M (-{pct:.0f}%)")

    print("\nFinal JSON:")
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, by_country, filtered, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for showing dramatic change between exactly two time points
        - **Country selection**: Top 12 destinations with both 2019 and 2020 data
        - **Highlights**:
            - Hong Kong: -94% (border closures)
            - Japan: -87%, South Korea: -86% (strict travel restrictions)
            - China: -81% (earliest and longest lockdowns)
            - France: -46% (relatively lower drop due to domestic tourism)
        - **Color**: by percentage decline (darker = steeper drop)
        """
    )
    return


if __name__ == "__main__":
    app.run()
