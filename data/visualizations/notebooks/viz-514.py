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
        # Primary School Grade Repetition Rates — Methodology

        Documents the data pipeline behind viz-514.
        Shows the fraction of primary school students who repeat a grade, 1990–2019.
        High repetition signals inefficiency in education systems and correlates with dropout risk.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-REPT-ZS.json"
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

    grid_data = []
    for code, years in by_country.items():
        pts = [{'y': y, 'v': round(v, 1)} for y, v in sorted(years.items()) if 1990 <= y <= 2019]
        if len(pts) < 5:
            continue
        max_val = max(p['v'] for p in pts)
        if max_val < 5:
            continue
        grid_data.append({
            'n': names[code],
            'pts': pts,
            'e': pts[0]['v'],
            'l': pts[-1]['v'],
            'max': max_val
        })

    grid_data.sort(key=lambda x: -x['max'])
    top24 = grid_data[:24]
    print(f"Selected {len(top24)} countries for grid")
    for g in top24[:5]:
        print(f"  {g['n']}: max={g['max']:.1f}%, n={len(g['pts'])}")
    return by_country, grid_data, is_country, names, top24


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — compact comparison of many time series at once
        - **Sorting**: Highest peak repetition rate first
        - **Key insights**: West and Central Africa have the highest rates (20–40%);
          Cambodia, Eritrea, and Burkina Faso show the sharpest declines;
          Belgium is the surprising European outlier, dropping from 16% to 2%
        - **Color**: Warm (high) to cool (low) by peak rate
        """
    )
    return


@app.cell
def _(json, top24):
    out = [{'n': g['n'], 'pts': g['pts'], 'e': g['e'], 'l': g['l'], 'max': g['max']} for g in top24]
    print(json.dumps(out, separators=(",", ":")))
    return (out,)


if __name__ == "__main__":
    app.run()
