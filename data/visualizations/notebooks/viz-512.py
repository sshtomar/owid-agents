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
        # Child Mortality Gender Gap — Methodology

        Scatter plot comparing male vs female under-5 mortality rates
        across 91 countries in 2023, revealing the near-universal biological
        disadvantage for boys.
        """
    )
    return


@app.cell
def _(json, mo):
    fe_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-MORT-FE.json"
    ma_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-MORT-MA.json"
    fe_data = json.loads(fe_path.read_text())["data"]
    ma_data = json.loads(ma_path.read_text())["data"]
    print(f"Female: {len(fe_data)} pts, Male: {len(ma_data)} pts")
    return fe_data, ma_data


@app.cell
def _(fe_data, ma_data):
    excl = ['World', ' income', 'countries', 'states', 'Africa', 'Asia', 'Europe',
            'Latin', 'Pacific', 'Arab', 'Caribbean', 'OECD', 'dividend', 'IDA',
            'IBRD', 'Fragile', 'Heavily', 'Small', 'Central', 'Euro ', 'North America',
            'South Asia', 'blend', 'East and']
    def is_country(name):
        return not any(x.lower() in name.lower() for x in excl)
    fe_2023 = {r['countryName']: r['value'] for r in fe_data if r.get('year') == 2023 and r.get('value') is not None and is_country(r['countryName'])}
    ma_2023 = {r['countryName']: r['value'] for r in ma_data if r.get('year') == 2023 and r.get('value') is not None and is_country(r['countryName'])}
    both = set(fe_2023.keys()) & set(ma_2023.keys())
    filtered = [{'n': n, 'f': round(fe_2023[n], 1), 'm': round(ma_2023[n], 1)} for n in sorted(both)]
    filtered.sort(key=lambda x: -(x['f'] + x['m']))
    print(f"Countries with both 2023 values: {len(filtered)}")
    female_higher = [r for r in filtered if r['f'] > r['m']]
    print(f"Countries where female > male: {len(female_higher)} ({[r['n'] for r in female_higher]})")
    return (filtered,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Scatter plot with diagonal reference line
        - **Axes**: x = female U5 mortality, y = male U5 mortality; points above diagonal = boys die more
        - **Color**: orange for normal (male > female), purple for anomalous (India: female > male, indicating gender bias)
        - **Dot size**: proportional to total mortality burden
        - **Insight**: Almost all countries cluster above the diagonal; India is the only exception, reflecting healthcare access bias against girls
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
