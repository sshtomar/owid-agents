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
        # Population Density Trends 1990–2022 — Methodology

        Sparkline grid showing population density (people per sq km) for 15 major countries
        from 1990 to 2022. Sorted by 2022 density. Bangladesh and South Korea are at
        the dense end; Brazil and Argentina at the sparse end.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EN-POP-DNST.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    major_countries = [
        'China', 'India', 'United States', 'Indonesia', 'Pakistan', 'Brazil', 'Nigeria',
        'Bangladesh', 'Ethiopia', 'Japan', 'Philippines', 'Congo, Dem. Rep.',
        'Mexico', 'Germany', 'United Kingdom', 'France', 'Italy', 'South Africa',
        'Kenya', 'Vietnam', 'Korea, Rep.', 'Egypt, Arab Rep.', 'Turkey', 'Tanzania',
        'Spain', 'Uganda', 'Colombia', 'Argentina', 'Thailand', 'Sudan'
    ]

    def is_aggregate(name):
        agg_words = ['World', 'income', 'dividend', 'Asia &', 'Africa ', 'Europe &',
                     'America', 'Arab World', 'Euro area', 'OECD', 'IDA', 'IBRD',
                     'heavily', 'Pacific', 'Caribbean', 'small states', 'Sub-Saharan',
                     'Middle East', 'South Asia', 'North America', 'classified']
        return any(w.lower() in name.lower() for w in agg_words)

    by_country = {}
    for r in data:
        if r['value'] and not is_aggregate(r['countryName']):
            by_country.setdefault(r['country'], {'name': r['countryName'], 'years': {}})['years'][r['year']] = r['value']

    sparklines = []
    for cc, info in by_country.items():
        name = info['name']
        if any(m.lower() in name.lower() for m in major_countries):
            series = [round(info['years'].get(yr) or 0, 1) for yr in range(1990, 2023)]
            if all(v > 0 for v in series):
                sparklines.append({'n': name, 's': series, 'e': round(series[0], 1), 'l': round(series[-1], 1), 'y0': 1990})

    sparklines.sort(key=lambda x: -x['l'])
    print(f"Countries: {len(sparklines)}")
    for sp in sparklines:
        print(f"  {sp['n']}: {sp['e']} -> {sp['l']} people/km2")
    return sparklines, by_country, major_countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — compact comparison across many countries
        - **Countries**: 15 major economies with complete 1990–2022 data
        - **Sort**: By 2022 density (highest first) — Bangladesh first, Argentina last
        - **Story**: Bangladesh grew from 858 to 1,300 people/km2. Japan and Germany
          peaked and are now declining as populations shrink.
        """
    )
    return


@app.cell
def _(json, sparklines):
    print(json.dumps(sparklines, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
