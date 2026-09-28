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
        # Renewable Energy Consumption (% of Total Final Energy) -- Methodology

        Sparkline grid comparing renewable energy's share of total final energy consumption
        for 7 countries from 1990 to 2021. Uses World Bank indicator EG.FEC.RNEW.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-FEC-RNEW-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    from collections import defaultdict
    target = ['China', 'Germany', 'Brazil', 'India', 'France', 'Japan', 'Indonesia']
    by_country = defaultdict(dict)
    for x in filtered:
        if x['countryName'] in target:
            by_country[x['countryName']][x['year']] = round(x['value'], 2)
    countries = list(by_country.keys())
    all_years = sorted(set(y for yvals in by_country.values() for y in yvals.keys()))
    print(f"Countries: {len(countries)}, Year range: {all_years[0]}-{all_years[-1]}")
    for c in target:
        if c in by_country:
            ys = sorted(by_country[c].keys())
            print(f"  {c}: {by_country[c][ys[0]]:.1f}% ({ys[0]}) -> {by_country[c][ys[-1]]:.1f}% ({ys[-1]})")
    return all_years, by_country, countries, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid -- 7 countries in a 4-column layout, each showing
          the full 1990-2021 trend in a compact cell.
        - **Country selection**: Mix of large emitters (China, India, Indonesia) showing
          declining renewables share as fossil fuel use grew, vs. European economies (Germany,
          France) showing policy-driven growth. Brazil included for contrast as it maintains
          high share via hydropower.
        - **Time range**: 1990-2021 (full SE4ALL dataset range)
        - **Highlights**: Germany rose from 2% to 18%; China fell from 34% to 15% as coal
          powered its industrial expansion; Brazil stayed consistently above 40% via hydro.
        """
    )
    return


@app.cell
def _(json, by_country, target):
    chart_data = []
    for c in target:
        if c not in by_country:
            continue
        years = sorted(by_country[c].keys())
        vals = [by_country[c][y] for y in years]
        chart_data.append({"n": c, "y0": years[0], "s": vals})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
