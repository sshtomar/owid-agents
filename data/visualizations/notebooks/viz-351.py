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
        # Decade of Financial Inclusion — Methodology

        Slope chart comparing bank/mobile-money account ownership in 2011 vs 2021,
        highlighting how mobile money transformed access in East Africa and South Asia.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--FX-OWN-TOTL-ZS.json"
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
        'Sub-Saharan Africa (IDA & IBRD countries)','Upper middle income','World',
        'European Union'
    }
    by_country = {}
    for row in data:
        if row['countryName'] not in aggregates and row['value'] is not None:
            key = row['countryName']
            year = row['year']
            if key not in by_country:
                by_country[key] = {}
            by_country[key][year] = round(row['value'], 1)

    slope_data = [
        (name, vals[2011], vals.get(2021, vals.get(2022, vals.get(2020))))
        for name, vals in by_country.items()
        if 2011 in vals and (2021 in vals or 2022 in vals or 2020 in vals)
    ]
    slope_data.sort(key=lambda x: -(x[2] - x[1]) if x[2] else 0)
    print(f"Countries with both 2011 and 2021 data: {len(slope_data)}")
    print("Top gainers:")
    for name, a, b in slope_data[:10]:
        print(f"  {name}: {a}% -> {b}% (+{b-a:.1f}pp)")
    return aggregates, by_country, slope_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — 2011 vs 2021 to show a decade of change clearly
        - **Country selection**: Mix of biggest gainers (India, Kenya, Ghana, Bolivia), still-low (Afghanistan, Congo D.R., Nigeria), and already-high (Germany) for contrast
        - **Color**: Green spectrum for high gains, amber for moderate, grey for stagnation
        - **Story**: Mobile banking (M-Pesa in Kenya, Aadhaar+UPI in India) drove dramatic jumps; some countries remain near 10% a decade later
        - **Note**: Mobile money counted since 2014 survey; explains some jumps in African nations
        """
    )
    return


@app.cell
def _(json, slope_data):
    selected = [
        'India','Kenya','Chile','Bolivia','Ghana','Indonesia','Cameroon',
        'Argentina','Kazakhstan','Brazil','South Africa','Bangladesh',
        'Tanzania','Germany','Thailand','Nigeria','Congo, Dem. Rep.','Afghanistan'
    ]
    chart_data = [
        {"n": name, "a": a, "b": b}
        for name, a, b in slope_data
        if name in selected and b is not None
    ]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
