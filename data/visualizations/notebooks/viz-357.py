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
        # PM2.5 Air Pollution Trends — Methodology

        Trend lines showing mean annual PM2.5 exposure (μg/m³) for 13 countries, 1990–2020.
        Data from World Bank indicator EN.ATM.PM25.MC.M3 (Global Burden of Disease Study).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-ATM-PM25-MC-M3.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    EXCLUDE_CODES = {
        'ZF','ZG','ZH','ZI','ZJ','ZQ','ZT','XC','XD','XE','XF','XG','XH',
        'XI','XJ','XL','XM','XN','XO','XP','XQ','XT','XU','B8','F1','OE',
        'S1','S2','S3','S4','T2','T3','T4','T5','T6','T7','V1','V2','V3','V4',
        'Z4','Z7','EU','1A','1W','4E','7E','8S'
    }

    def is_real_country(d):
        code = d['country']
        return code.isalpha() and len(code) == 2 and code not in EXCLUDE_CODES

    from collections import defaultdict
    filtered = [d for d in data if is_real_country(d) and d['value'] is not None]
    by_country = defaultdict(dict)
    for d in filtered:
        by_country[d['countryName']][d['year']] = d['value']
    print(f"Real countries: {len(by_country)}")
    return by_country, filtered, is_real_country


@app.cell
def _(by_country, json):
    # Selected countries and years for the chart
    selected = [
        ('India', 'India'), ('China', 'China'), ('Bangladesh', 'Bangladesh'),
        ('Egypt, Arab Rep.', 'Egypt'), ('Ghana', 'Ghana'),
        ('Iran, Islamic Rep.', 'Iran'), ('Indonesia', 'Indonesia'),
        ('Brazil', 'Brazil'), ('Germany', 'Germany'), ('France', 'France'),
        ('Japan', 'Japan'), ('Australia', 'Australia'), ('Finland', 'Finland'),
    ]
    years = [1990, 1995, 2000, 2005, 2010, 2015, 2020]

    chart_data = []
    for country_key, short_name in selected:
        if country_key not in by_country:
            continue
        vals = by_country[country_key]
        series = []
        for y in years:
            v = vals.get(y, vals.get(y-1, vals.get(y+1)))
            series.append(round(v, 1) if v is not None else None)
        chart_data.append({'n': short_name, 's': series, 'y0': 1990, 'step': 5})
        print(f"{short_name}: {series}")

    print("\nFinal JSON:")
    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — best for showing temporal evolution across many countries simultaneously
        - **Country selection**: 13 countries spanning the full range from Finland (~5) to India/Egypt (~55-65 μg/m³)
        - **Time range**: 1990–2020 at 5-year intervals; covers pre/post-policy shifts
        - **Highlights**:
            - China: sharp drop after 2015 clean air policy
            - Europe (Germany, France): roughly halved PM2.5 since 1990
            - India/Bangladesh: elevated throughout, with high 2015 readings
            - Indonesia: steady decline from 30 to 18 μg/m³
        - **Reference line**: WHO interim target 3 at 15 μg/m³
        - **Color**: by 2020 level (warm = high pollution, cool = lower pollution)
        """
    )
    return


if __name__ == "__main__":
    app.run()
