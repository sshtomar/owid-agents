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
        # Domestic Freshwater Use Share: 1990 vs 2020 — Methodology

        Documents the data pipeline behind viz-513.
        Shows what % of total freshwater withdrawals go to household/domestic use.
        Agricultural nations have very low domestic %; urban/island nations have high domestic %.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-H2O-FWDM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    agg_words = ['Africa', 'Asia', 'Europe', 'income', 'dividend', 'IDA', 'IBRD',
                 'states', 'situations', 'blend', 'Pacific', 'Caribbean', 'Euro',
                 'Latin', 'Middle', 'Eastern', 'Western', 'Central', 'Southern',
                 'Northern', 'OECD', 'World', 'classification', 'G7',
                 'heavily', 'America', 'area', 'region', 'countries']

    def is_country(name):
        return not any(w.lower() in name.lower() for w in agg_words)

    by_country = defaultdict(dict)
    names = {}
    for p in data:
        if p.get('value') is not None and p.get('countryName') and is_country(p['countryName']):
            by_country[p['country']][p['year']] = p['value']
            names[p['country']] = p['countryName']

    def find_closest(years_dict, target, window=8):
        for offset in range(window):
            if target + offset in years_dict:
                return years_dict[target + offset]
            if offset > 0 and target - offset in years_dict:
                return years_dict[target - offset]
        return None

    selected = [
        'Djibouti', 'Jamaica', 'Bolivia', 'Benin', 'Congo, Rep.', 'Bahrain',
        'Ireland', 'Jordan', 'Israel', 'Germany', 'Angola', 'Botswana',
        'Denmark', 'El Salvador', 'Czechia',
        'India', 'Iran, Islamic Rep.', 'Indonesia', 'Chile', 'Afghanistan'
    ]

    out = []
    for code, years in by_country.items():
        a = find_closest(years, 1990, 8)
        b = find_closest(years, 2020, 6)
        if a is not None and b is not None and names[code] in selected:
            out.append({'n': names[code], 'a': round(a, 1), 'b': round(b, 1)})

    out.sort(key=lambda x: -x['b'])
    print(f"Slope pairs: {len(out)}")
    for s in out:
        print(f"  {s['n']}: {s['a']:.1f}% -> {s['b']:.1f}%")
    return agg_words, by_country, find_closest, is_country, names, out, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compare 1990 vs ~2020, showing direction of change
        - **Story**: Huge divergence — Bolivia jumped from 9% to 70% (agricultural water use declined);
          Afghanistan has stayed at 1% (nearly all water is for irrigation);
          Countries with little agriculture (Djibouti, Caribbean islands) have high domestic shares
        - **Color**: Magnitude of change; large increases = orange/red; small change = green
        """
    )
    return


@app.cell
def _(json, out):
    print(json.dumps(out, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
