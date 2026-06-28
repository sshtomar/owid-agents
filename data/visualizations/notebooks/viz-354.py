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
        # Financial Inclusion: Account Ownership 2011 vs 2021 -- Methodology

        Slope chart comparing the share of adults (15+) owning an account at a
        financial institution or mobile-money provider, showing the decade of
        inclusion progress 2011-2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FX-OWN-TOTL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    target_countries = [
        'Cambodia', 'Guinea', "Congo, Dem. Rep.", 'Afghanistan', 'Chad', 'Egypt, Arab Rep.',
        'Armenia', 'Jordan', 'Bolivia', 'Ghana', 'Colombia', 'Bangladesh', 'India',
        'Kenya', 'Brazil', 'China', 'Iran, Islamic Rep.', 'Japan', 'Germany',
    ]

    by_country = defaultdict(dict)
    for x in data:
        if x['countryName'] in target_countries and x['value'] is not None:
            by_country[x['countryName']][x['year']] = x['value']

    slope = []
    for name in target_countries:
        yrs = by_country.get(name, {})
        a = yrs.get(2011)
        b = yrs.get(2021) or yrs.get(2022)
        if a is not None and b is not None:
            display = name.replace(', Arab Rep.', '').replace(', Dem. Rep.', ' DR').replace(', Islamic Rep.', '')
            slope.append({'n': display, 'a': round(a, 1), 'b': round(b, 1)})

    slope.sort(key=lambda x: x['a'])
    print(f"Series: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']}% -> {s['b']}% (+{s['b']-s['a']:.1f}pp)")
    return slope, by_country, target_countries


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2011 vs 2021)
        - **Color**: Dark green for big gains (>30pp), light green for moderate (15-30pp),
          grey for minimal gains (<15pp), red for near-stagnant (<5pp)
        - **Story**: India surged from 35% to 78%, Kenya from 42% to 79% (mobile money).
          Afghanistan barely moved (9% to 10%), Chad from 9% to 24%.
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
