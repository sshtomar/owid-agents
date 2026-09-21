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
        # Depression Prevalence 2015 -- Methodology

        Horizontal bar chart of estimated depression prevalence for 25 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--GDO_q35.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    iso_map = {
        'UKR': 'Ukraine', 'AUS': 'Australia', 'EST': 'Estonia', 'USA': 'United States',
        'BRA': 'Brazil', 'GRC': 'Greece', 'PRT': 'Portugal', 'LTU': 'Lithuania',
        'FIN': 'Finland', 'BLR': 'Belarus', 'LKA': 'Sri Lanka',
        'DEU': 'Germany', 'ESP': 'Spain', 'JPN': 'Japan', 'KOR': 'South Korea',
        'CHN': 'China', 'IND': 'India', 'MEX': 'Mexico', 'ARG': 'Argentina',
        'TUR': 'Turkey', 'KEN': 'Kenya', 'THA': 'Thailand', 'IRN': 'Iran',
        'NPL': 'Nepal', 'AFG': 'Afghanistan', 'SLB': 'Solomon Islands',
        'PNG': 'Papua New Guinea', 'TLS': 'Timor-Leste',
    }
    chart_data = []
    for pt in data:
        cc = pt['country']
        val = pt.get('value')
        if val is not None and cc in iso_map:
            chart_data.append({'n': iso_map[cc], 'v': round(val, 2)})
    chart_data.sort(key=lambda x: x['v'])

    # Select 25: bottom 5, diverse middle, top 10
    bottom5 = chart_data[:5]
    top10 = chart_data[-10:]
    middle = [x for x in chart_data[5:-10] if x['n'] in [
        'Mexico', 'China', 'Japan', 'Thailand', 'Turkey', 'Kenya', 'India', 'Argentina', 'Iran', 'Germany']]
    selected = (bottom5 + middle + top10)
    selected.sort(key=lambda x: x['v'])

    print(f"Selected {len(selected)} countries")
    for c in selected:
        print(f"  {c['n']}: {c['v']}%")
    print(json.dumps(selected, separators=(',', ':')))
    return (selected,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — single-year data, ranking is the story
        - **Country selection**: Pacific island nations at the low end, Eastern European and English-speaking nations at the high end, diverse middle
        - **Story**: Depression burden is higher in high-income countries; Eastern Europe shows elevated rates possibly reflecting post-Soviet social disruption; Pacific islands and South/Southeast Asia show notably lower rates
        - **Caveat**: Estimates depend on measurement methodology and may reflect detection/diagnosis gaps as much as true prevalence differences
        """
    )
    return


if __name__ == "__main__":
    app.run()
