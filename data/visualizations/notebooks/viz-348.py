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
        # Scientific Output Explosion — Methodology

        Tracks the dramatic rise in scientific journal articles, with China's
        27x growth from 1996 to 2022 as the central story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-JRN-ARTC-SC.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    target = {'China','India','Germany','Japan','Korea, Rep.','France','Italy','Canada','Brazil','Iran, Islamic Rep.','Indonesia','Australia'}
    filtered = [d for d in data if d['countryName'] in target and d['value'] is not None]
    print(f"After filtering: {len(filtered)} rows")
    countries = sorted(set(d['countryName'] for d in filtered))
    years = sorted(set(d['year'] for d in filtered))
    print(f"Countries: {len(countries)}, Year range: {years[0]}-{years[-1]}")
    return countries, filtered, target, years


@app.cell
def _(filtered):
    values = [d['value'] for d in filtered]
    print(f"Value range: {min(values):.0f} - {max(values):.0f} articles/year")
    china_1996 = next(d['value'] for d in filtered if d['countryName'] == 'China' and d['year'] == 1996)
    china_2022 = next(d['value'] for d in filtered if d['countryName'] == 'China' and d['year'] == 2022)
    print(f"China 1996: {china_1996:,.0f}, 2022: {china_2022:,.0f} ({china_2022/china_1996:.1f}x growth)")
    return china_1996, china_2022, values


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — annual data 1996-2022, 12 countries
        - **Country selection**: Top scientific publishers excluding aggregates; US data not available in this dataset
        - **Highlight**: China colored red and thicker stroke — its rise is the headline story
        - **Y axis**: In thousands (k) to keep labels readable; China approaches 900k
        - **Story**: China went from 7th place in 1996 to dominant leader by 2019; India also rising fast
        """
    )
    return


@app.cell
def _(json, filtered):
    chart_data = [
        {"n": d["countryName"], "y": d["year"], "v": round(d["value"])}
        for d in sorted(filtered, key=lambda x: (x["countryName"], x["year"]))
    ]
    print(json.dumps(chart_data[:5], separators=(",", ":")))
    print(f"... ({len(chart_data)} total rows)")
    return (chart_data,)


if __name__ == "__main__":
    app.run()
