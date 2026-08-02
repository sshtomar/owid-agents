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
        # Intentional Homicides: 2000 vs. 2022 -- Methodology

        Slope chart comparing intentional homicide rates (per 100,000 people)
        in 2000 and 2022. Highlights El Salvador's unprecedented decline and
        several Caribbean nations worsening over the period.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-IHR-PSRC-P5.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    SKIP_WORDS = ['World', 'income', 'members', 'dividend', 'Asia', 'Africa',
                   'Europe', 'America', 'Carib', 'Middle East', 'Pacific',
                   'IBRD', 'IDA', 'OECD', 'Union', 'area', 'states', 'countries',
                   'Least developed', 'HIPC', 'Heavily', 'small states', 'North America']

    def is_country(code, name):
        if len(code) != 2: return False
        if code[0].isdigit(): return False
        for w in SKIP_WORDS:
            if w.lower() in name.lower(): return False
        return True

    by_country = {}
    for row in data:
        code = row['country']
        name = row['countryName']
        if row['value'] is not None and is_country(code, name):
            y = row['year']
            if name not in by_country:
                by_country[name] = {}
            by_country[name][y] = row['value']

    both = [(c, vs.get(2000), vs.get(2022)) for c, vs in by_country.items()
            if vs.get(2000) is not None and vs.get(2022) is not None]

    KEEP = {
        'Colombia', 'El Salvador', 'Honduras', 'Jamaica', 'Dominica',
        'Ecuador', 'Belize', 'Costa Rica', 'Brazil', 'Dominican Republic',
        'Bahamas, The', 'Kazakhstan', 'Estonia', 'Bulgaria', 'Albania',
        'India', 'Finland', 'Canada', 'Croatia', 'Hungary'
    }

    slope = []
    for c, a, b in both:
        if c in KEEP:
            slope.append({'n': c.replace(', The', '').replace('Dominican Republic', 'Dominican Rep.'), 'a': round(a, 2), 'b': round(b, 2)})
    slope.sort(key=lambda x: x['a'])

    print(f"Series: {len(slope)}")
    for s in slope:
        delta = s['b'] - s['a']
        print(f"  {s['n']}: {s['a']} -> {s['b']} ({delta:+.1f})")
    return slope, by_country, both, KEEP


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart (2000 vs. 2022) — best for showing direction and magnitude of change
        - **Country selection**: 20 countries spanning the full range of outcomes
        - **Color encoding**: Green for decline, red for increase; saturation encodes magnitude
        - **Key insight**: El Salvador dropped from 59.7 to 7.9 (Bukele anti-gang policies, 2022)
          Jamaica rose from 34 to 53.1; Dominica from 2.9 to 28.4 (most % increase)
        - **Scale**: 0–70 to accommodate Colombia (2000) at 67.9
        """
    )
    return


@app.cell
def _(json, slope):
    print(json.dumps(slope, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
