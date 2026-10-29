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
        # Contraceptive Prevalence — Methodology

        Documents the data pipeline behind viz-511.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-CONM-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_keywords = ['World', 'Africa', 'Asia', 'Europe', 'OECD', 'income', 'dividend', 'Arab',
                    'Caribbean', 'Pacific', 'Latin', 'Sub-Saharan', 'Middle East', 'North America',
                    'Fragile', 'IDA', 'IBRD', 'Heavily', 'Least', 'Small', 'states', 'South Asia',
                    'FCV', 'Conflict', 'blend', 'region']
    by_country = {}
    for row in data:
        c = row['countryName']
        if any(kw.lower() in c.lower() for kw in agg_keywords):
            continue
        if row['value'] is None:
            continue
        if c not in by_country:
            by_country[c] = {}
        by_country[c][row['year']] = row['value']
    print(f"Individual countries: {len(by_country)}")
    return agg_keywords, by_country


@app.cell
def _(by_country):
    selected = [
        'China', 'Finland', 'Colombia', 'Ecuador', 'Honduras', 'Brazil', 'India',
        'Kenya', 'Bangladesh', 'Indonesia', 'Eswatini', 'Ethiopia',
        'Ghana', 'Congo, Dem. Rep.', 'Cameroon', 'Guinea',
        'Egypt, Arab Rep.'
    ]
    result = []
    for c in selected:
        if c not in by_country:
            continue
        years = by_country[c]
        ys = sorted(years.keys())
        near90 = min((y for y in ys if 1985 <= y <= 1998), key=lambda y: abs(y - 1990), default=None)
        near20 = max((y for y in ys if y >= 2015), default=max(ys))
        if near90 and near20 and near90 != near20:
            display = c.replace('Egypt, Arab Rep.', 'Egypt').replace('Congo, Dem. Rep.', 'DR Congo')
            result.append({'n': display, 'a': round(years[near90], 1), 'b': round(years[near20], 1)})
    result.sort(key=lambda x: -x['b'])
    print(f"Countries in chart: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['a']} -> {r['b']}")
    return result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points (~1990 vs ~2015/2022) show direction of change
        - **Country selection**: Spans from high-use (Finland, China, Brazil) to very low (Guinea, DR Congo)
        - **Highlight**: Sub-Saharan Africa started near zero but most have doubled or tripled access
        - **Note**: Values show % of married women aged 15-49 using any modern contraceptive method
        """
    )
    return


@app.cell
def _(json, result):
    print(json.dumps(result, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
