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
        # NCD Deaths Share 2000 vs 2021 — Methodology

        Slope chart showing non-communicable disease share of total deaths for
        30 countries in 2000 and 2021. Illustrates the global epidemiological transition.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DTH-NCOM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    from collections import defaultdict
    skip_patterns = ['Eastern','Western and Central','Arab World','Caribbean',
        'Central Europe','Early-demographic','East Asia','Europe &','High income',
        'Latin America','Low &','Low income','Middle income','North America','OECD',
        'South Asia','Sub-Saharan','World','IDA','IBRD',' income','Pacific',
        'dividend','small states','Baltics','emerging','developing','classification','demographic']
    def is_region(name):
        return any(p.lower() in name.lower() for p in skip_patterns)
    filtered = [r for r in data if r['value'] is not None and not is_region(r['countryName'])]
    by_country = defaultdict(dict)
    for r in filtered:
        by_country[r['countryName']][r['year']] = r['value']
    both = [(cn,v) for cn,v in by_country.items() if 2000 in v and 2021 in v]
    both.sort(key=lambda x: x[1][2021], reverse=True)
    print(f"Countries with 2000 and 2021: {len(both)}")
    return both, by_country


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — 2-point comparison (2000 vs 2021)
        - **Country selection**: Top 10 NCD share, 10 mid-range, bottom 10
        - **Color**: Green = high NCD share (advanced transition), amber/terra = low (infectious still dominant)
        - **50% reference line**: The crossing point between NCD and infectious mortality
        """
    )
    return


@app.cell
def _(both, json):
    top = both[:10]
    bottom = both[-10:]
    mid_pool = both[10:-10]
    step = max(1, len(mid_pool) // 10)
    mid = mid_pool[::step][:10]
    selected = sorted(set(cn for cn,_ in top+mid+bottom))
    records = [(cn, both_dict) for cn, both_dict in both if cn in selected]
    records.sort(key=lambda x: x[1][2021], reverse=True)
    chart_data = [{"n": cn, "a": round(vals[2000],1), "b": round(vals[2021],1)} for cn, vals in records]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
