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
        # Physicians per 1,000 People: ~2000 vs. ~2020 -- Methodology

        Slope chart comparing physician density across 16 countries between
        approximately 2000 and 2020. Uses the closest year within 5 years of
        each target year to maximize coverage. Highlights the persistent and
        vast gap between high-income and low-income countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-MED-PHYS-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_words = ['income', 'OECD', 'Euro ', 'Europe', 'Asia', 'Africa', 'America',
                     'Caribbean', 'East ', 'South Asia', 'West ', 'North America',
                     'Pacific', 'Global', 'IDA', 'IBRD', 'Fragile', 'Small',
                     'Landlocked', 'countries', 'Developing', 'states', 'dividend',
                     'members', 'Arab', 'Saharan', 'Sub-']
    by_country = {}
    for row in data:
        if row['value'] is None:
            continue
        n = row['countryName']
        if any(x in n for x in exclude_words):
            continue
        if n not in by_country:
            by_country[n] = {}
        by_country[n][row['year']] = row['value']

    def closest(yrs_dict, target):
        cands = [(abs(y-target), y, v) for y, v in yrs_dict.items() if abs(y-target) <= 5]
        if not cands:
            return None
        return sorted(cands)[0][2]

    selected = ['Cuba', 'Greece', 'Austria', 'Germany', 'Denmark', 'Argentina',
                'Georgia', 'Australia', 'Korea, Rep.', 'China', 'Brazil',
                'Bangladesh', 'Indonesia', 'Burkina Faso', 'Ethiopia', 'Chad']
    display_names = {'Korea, Rep.': 'Korea', 'Burkina Faso': 'Burkina F.'}

    chart_data = []
    for name in selected:
        if name not in by_country:
            continue
        v2000 = closest(by_country[name], 2000)
        v2020 = closest(by_country[name], 2020)
        if v2000 is None or v2020 is None:
            continue
        chart_data.append({'n': display_names.get(name, name),
                            'a': round(v2000, 2), 'b': round(v2020, 2)})

    chart_data.sort(key=lambda x: -x['b'])
    print(f"Countries: {len(chart_data)}")
    for d in chart_data:
        print(f"  {d['n']}: {d['a']} -> {d['b']}")
    return by_country, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points, shows universal improvement
        - **Year selection**: Closest year within 5 years of 2000 and 2020
        - **Country selection**: 16 countries spanning the full spectrum from 0.06 to 9.29
        - **Highlights**: Cuba leads at 9.29 per 1000; Chad at 0.06; all improved
        """
    )
    return


if __name__ == "__main__":
    app.run()
