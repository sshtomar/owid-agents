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
        # BCG Immunization Coverage — Methodology

        Sparkline grid showing BCG (tuberculosis vaccine) coverage for
        24 developing countries from 1990 to 2024.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IBCG.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict
    excl = ['World', 'income', 'states', 'Africa ', 'Asia ', 'Europe ', 'Latin ', 'Pacific',
            'Arab ', 'Caribbean', 'OECD', 'dividend', 'IDA ', 'IBRD', 'Fragile', 'Heavily',
            'Small', 'Euro area', 'North America', 'South Asia', 'blend', 'East and',
            'Pacific (excl', 'Central Europe', 'Least developed', 'Middle East, North', 'Sub-Saharan']
    def is_country(name):
        return not any(x in name for x in excl)
    series = defaultdict(dict)
    for r in data:
        n = r.get('countryName', '')
        if is_country(n) and r.get('value') is not None and r.get('year', 0) >= 1990:
            series[n][r['year']] = r['value']
    selected = ['India', 'Indonesia', 'Bangladesh', 'Ethiopia', 'Kenya', 'Ghana',
                'China', 'Brazil', 'Colombia', 'Afghanistan', 'Angola', 'Bolivia',
                'Cambodia', 'Cameroon', 'Burkina Faso', 'Chad', 'Congo, Dem. Rep.',
                "Cote d'Ivoire", 'Ecuador', 'Guatemala', 'Haiti', 'Honduras',
                'Iran, Islamic Rep.', 'Iraq']
    filtered = []
    for n in selected:
        if n in series:
            pts = sorted(series[n].items())
            filtered.append({'n': n, 's': [int(round(v, 0)) for _, v in pts], 'y0': pts[0][0], 'e': int(round(pts[0][1], 0)), 'l': int(round(pts[-1][1], 0))})
    print(f"Countries extracted: {len(filtered)}")
    return (filtered,)


@app.cell
def _(filtered):
    values = [(d['n'], d['e'], d['l'], d['l'] - d['e']) for d in filtered]
    values.sort(key=lambda x: -x[3])
    print("Biggest improvers:")
    for n, e, l, gain in values[:6]:
        print(f"  {n}: {e}% -> {l}% (+{gain})")
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — ideal for comparing many entities' trends simultaneously
        - **Country selection**: 24 high-population developing countries where BCG vaccination is a key public health tool
        - **Time range**: 1990-2024
        - **Insights**: Most countries achieved 80-99% coverage; Afghanistan and DRC had disruptions; Chad started at 59% and reached 92%
        - **Sort**: by latest coverage descending to surface high achievers first
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
