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
        # Primary School Enrollment Gains — Methodology

        Slope chart comparing primary school net enrollment (%) in 2000 vs 2015
        for 23 countries, showing the millennium development goal progress.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-PRM-NENR.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    excl = ['income', 'states', 'Africa', 'Asia', 'Europe', 'Latin', 'Pacific', 'Arab',
            'Caribbean', 'OECD', 'dividend', 'IDA', 'IBRD', 'Fragile', 'Heavily', 'Small',
            'Central', 'Euro ', 'North America', 'South Asia', 'Least developed', 'Middle East',
            'Sub-Saharan', 'World']
    def is_country(name):
        return not any(x in name for x in excl)
    c2000 = {r['countryName']: r['value'] for r in data if r.get('year') == 2000 and r.get('value') is not None and is_country(r['countryName'])}
    c2015 = {r['countryName']: r['value'] for r in data if r.get('year') == 2015 and r.get('value') is not None and is_country(r['countryName'])}
    both = set(c2000.keys()) & set(c2015.keys())
    result = [{'n': n, 'a': round(min(c2000[n], 100), 1), 'b': round(min(c2015[n], 100), 1)} for n in sorted(both)]
    result.sort(key=lambda x: x['a'])
    top_gain = sorted(result, key=lambda x: x['b'] - x['a'], reverse=True)[:15]
    near_universal = sorted(result, key=lambda x: -x['a'])[:8]
    selected_names = {r['n'] for r in top_gain} | {r['n'] for r in near_universal}
    filtered = [r for r in result if r['n'] in selected_names]
    filtered.sort(key=lambda x: x['a'])
    print(f"Countries: {len(filtered)}")
    print("Top gains:")
    for r in sorted(filtered, key=lambda x: x['b'] - x['a'], reverse=True)[:6]:
        print(f"  {r['n']}: {r['a']} -> {r['b']} (+{r['b']-r['a']:.1f})")
    return (filtered,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — ideal for before/after comparisons across many entities
        - **Country selection**: Countries with the biggest gains (Sub-Saharan Africa) plus near-universal countries (OECD) to show the full spectrum
        - **Color**: orange/amber for high gainers, green for moderate, gray for near-universal
        - **MDG context**: The 2000-2015 period coincides with Millennium Development Goal 2 (universal primary education), making these gains historically significant
        - **Highlights**: Ethiopia +44pp, Djibouti +34pp, Burkina Faso +33pp; Iran reached 99.7%
        """
    )
    return


@app.cell
def _(json, filtered):
    chart_data = filtered
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
