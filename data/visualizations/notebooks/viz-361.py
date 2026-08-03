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
        # Hydropower's Share of Electricity: 1990 vs. 2022 -- Methodology

        Slope chart comparing hydroelectric electricity share (% of total) for
        15 countries between 1990 and 2022. Reveals which historically hydro-
        dominant countries have diversified their electricity mix and which
        remain near 100% hydro-dependent.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-HYRO-ZS.json"
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
                     'members', 'Arab', 'Sub-', 'Organisation', 'World']
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

    selected = ['Congo, Dem. Rep.', 'Albania', 'Ethiopia', 'Costa Rica', 'Colombia',
                'Ecuador', 'Canada', 'Brazil', 'Norway', 'Cameroon', 'Austria',
                'Ghana', 'China', 'India', 'Germany', 'Australia']
    display_names = {'Congo, Dem. Rep.': 'DR Congo'}

    chart_data = []
    for name in selected:
        if name not in by_country:
            continue
        v1990 = by_country[name].get(1990)
        v2022 = by_country[name].get(2022) or by_country[name].get(2021) or by_country[name].get(2020)
        if v1990 is None or v2022 is None:
            continue
        chart_data.append({'n': display_names.get(name, name),
                            'a': round(v1990, 1), 'b': round(v2022, 1)})

    chart_data.sort(key=lambda x: -x['b'])
    print(f"Countries: {len(chart_data)}")
    for d in chart_data:
        print(f"  {d['n']}: {d['a']} -> {d['b']} ({d['b']-d['a']:+.1f})")
    return by_country, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — two time points show change in hydro dependency
        - **Year selection**: 1990 (baseline) vs. 2022 (most recent available)
        - **Country selection**: Countries with meaningful hydro share + comparison cases
        - **Highlights**: Ghana fell from 100% to 35%; Brazil from 93% to 63%;
          DR Congo, Albania, Ethiopia remain hydro-dominant; China/India grew other sources
        """
    )
    return


if __name__ == "__main__":
    app.run()
