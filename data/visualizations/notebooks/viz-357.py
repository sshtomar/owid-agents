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
        # Pupil-Teacher Ratio in Primary Schools, 1990 vs 2015 -- Methodology

        Slope chart comparing pupils per teacher in primary school in 1990 versus 2015.
        Highlights which countries reduced classroom crowding and which saw conditions worsen.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-ENRL-TC-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_terms = ['World','income','region','dividend',' Asia',' Africa',' Europe',' America',
                 'Latin','Arab',' Pacific','Central ','East Asia','South Asia','Sub-Saharan',
                 'Sub-','Low-','High-','Middle-','OECD','IDA','IBRD','Fragile','small state',
                 'Euro area','Euro ','developing','emerging','post-','pre-','early-','upper-',
                 'lower-','HIPC','Caribbean','North America','Heavily','Least developed','European Union']
    def is_country(name):
        return not any(t.lower() in name.lower() for t in agg_terms)

    countries = [x for x in data if x['value'] is not None and is_country(x['countryName'])]
    c1990 = {x['countryName']: x['value'] for x in countries if x['year'] == 1990}
    c2015 = {x['countryName']: x['value'] for x in countries if x['year'] == 2015}
    both = [(c, round(c1990[c],1), round(c2015[c],1)) for c in c1990 if c in c2015]
    print(f"Countries with data in both 1990 and 2015: {len(both)}")
    return both, c1990, c2015, countries, is_country


@app.cell
def _(both):
    name_map = {
        'Korea, Rep.': 'South Korea',
        "Cote d'Ivoire": "Cote d'Ivoire",
        'Gambia, The': 'Gambia',
        'Cabo Verde': 'Cape Verde',
    }
    def clean(n):
        return name_map.get(n, n)

    selected = [
        'Chad','Burundi','Burkina Faso','Cameroon','Benin','Djibouti',
        "Cote d'Ivoire",'Gambia, The','Cambodia','Afghanistan','Eritrea',
        'Korea, Rep.','Costa Rica','Jamaica','Ecuador','Colombia',
        'Greece','Algeria','Kazakhstan','Cuba','Cyprus','China','Bahrain','Austria','Italy'
    ]

    slope = [{'n': clean(c), 'a': a, 'b': b} for c,a,b in both if c in selected]
    slope.sort(key=lambda x: -x['a'])
    print(f"Series: {len(slope)}")
    for s in slope:
        print(f"  {s['n']}: {s['a']} -> {s['b']} (change: {s['b']-s['a']:+.1f})")
    return clean, selected, slope


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (1990 vs 2015) to highlight two-decade improvement
        - **Color**: Red for countries where ratio worsened, green gradient for improvement
        - **Story**: Sub-Saharan Africa still carries the highest loads (Chad: 67 students/teacher),
          while South Korea (36 -> 17) and Costa Rica (32 -> 13) show dramatic reductions.
          Several West African countries actually worsened: Benin, Cambodia, Cote d'Ivoire.
        - **Selection**: 25 countries spanning the full range from 10 to 67 pupils per teacher
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
