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
        # Population Growth Rate Divergence — Methodology

        Explores the demographic divide between fast-growing Sub-Saharan Africa
        and slow/shrinking Europe, with Asia's ongoing transition in between.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregates = {
        'Africa Eastern and Southern','Africa Western and Central','Arab World',
        'Caribbean small states','Central Europe and the Baltics','Early-demographic dividend',
        'East Asia & Pacific','East Asia & Pacific (excluding high income)',
        'East Asia & Pacific (IDA & IBRD countries)','Euro area','Europe & Central Asia',
        'Europe & Central Asia (excluding high income)','Europe & Central Asia (IDA & IBRD countries)',
        'Fragile and conflict affected situations','Heavily indebted poor countries (HIPC)',
        'High income','IBRD only','IDA & IBRD total','IDA blend','IDA only','IDA total',
        'Late-demographic dividend','Latin America & Caribbean',
        'Latin America & Caribbean (excluding high income)',
        'Latin America & the Caribbean (IDA & IBRD countries)',
        'Least developed countries: UN classification','Low & middle income','Low income',
        'Lower middle income','Middle East & North Africa',
        'Middle East & North Africa (excluding high income)',
        'Middle East & North Africa (IDA & IBRD countries)','Middle income','North America',
        'Not classified','OECD members','Other small states','Pacific island small states',
        'Post-demographic dividend','Pre-demographic dividend','Small states','South Asia',
        'South Asia (IDA & IBRD)','Sub-Saharan Africa','Sub-Saharan Africa (excluding high income)',
        'Sub-Saharan Africa (IDA & IBRD countries)','Upper middle income','World'
    }
    target_countries = {
        'Chad', 'Niger', 'Ethiopia', 'Kenya', 'Congo, Dem. Rep.',
        'Bangladesh', 'India', 'Indonesia', 'Brazil', 'China',
        'Germany', 'Italy', 'Bulgaria'
    }
    filtered = [
        d for d in data
        if d['countryName'] in target_countries
        and d['value'] is not None
        and d['year'] % 5 == 0
        and 1965 <= d['year'] <= 2020
    ]
    print(f"After filtering: {len(filtered)} rows")
    return filtered, target_countries, aggregates


@app.cell
def _(filtered):
    countries = sorted(set(d['countryName'] for d in filtered))
    years = sorted(set(d['year'] for d in filtered))
    values = [d['value'] for d in filtered]
    print(f"Countries: {len(countries)}, Years: {years[0]}-{years[-1]}")
    print(f"Value range: {min(values):.2f} - {max(values):.2f} %/yr")
    return countries, years, values


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows continuous trajectories over 55 years
        - **Country selection**: 5 fast-growing SSA, 3 South Asian (showing rapid decline), 3 major economies (diverse), 3 European (flat/negative)
        - **Time range**: 1965-2020, every 5 years to keep data manageable
        - **Color groups**: Red=SSA fast, Orange=South Asia slowing, Blue=major economies, Grey=Europe flat/negative
        - **Story**: The demographic gap is *widening*, not narrowing — Africa's growth is accelerating while Europe goes negative
        """
    )
    return


@app.cell
def _(json, filtered):
    chart_data = [
        {"n": d["countryName"], "y": d["year"], "v": round(d["value"], 3)}
        for d in sorted(filtered, key=lambda x: (x["countryName"], x["year"]))
    ]
    print(json.dumps(chart_data[:10], separators=(",", ":")))
    print(f"... ({len(chart_data)} total rows)")
    return (chart_data,)


if __name__ == "__main__":
    app.run()
