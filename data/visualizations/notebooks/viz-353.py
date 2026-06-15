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
        # Measles Immunization Coverage — Methodology

        Sparkline grid showing measles vaccine coverage (1990–2023) for 23 countries.
        Ordered from worst to best 2023 coverage to tell the full range of the story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-MEAS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    agg_set = {
        'Africa Eastern and Southern','Africa Western and Central','Arab World',
        'Caribbean small states','Central Europe and the Baltics','East Asia & Pacific',
        'East Asia & Pacific (excluding high income)','East Asia and Pacific (IDA & IBRD countries)',
        'Euro area','Europe & Central Asia','Europe & Central Asia (IDA & IBRD countries)',
        'Europe & Central Asia (excluding high income)','European Union',
        'Fragile and conflict affected situations','Heavily indebted poor countries (HIPC)',
        'High income','IBRD only','IDA & IBRD total','IDA blend','IDA only','IDA total',
        'Late-demographic dividend','Early-demographic dividend','Latin America & Caribbean',
        'Latin America & Caribbean (excluding high income)',
        'Latin America and the Caribbean (IDA & IBRD countries)',
        'Least developed countries: UN classification','Low & middle income','Low income',
        'Lower middle income','Middle East & North Africa',
        'Middle East & North Africa (excluding high income)',
        'Middle East & North Africa (IDA & IBRD countries)','Middle income','North America',
        'Not classified','OECD members','Other small states','Pacific island small states',
        'Post-demographic dividend','Pre-demographic dividend','Small states','South Asia',
        'South Asia (IDA & IBRD)','Sub-Saharan Africa',
        'Sub-Saharan Africa (IDA & IBRD countries)',
        'Sub-Saharan Africa (excluding high income)','Upper middle income',
        'West Bank and Gaza','World'
    }
    pts = {}
    for p in data:
        cn = p['countryName']
        if cn in agg_set or p['value'] is None:
            continue
        pts.setdefault(cn, {})[p['year']] = p['value']
    print(f"Individual countries: {len(pts)}")
    return agg_set, pts


@app.cell
def _(pts):
    selected = [
        'Central African Republic','Congo, Dem. Rep.','Guinea','Benin','Afghanistan',
        'Equatorial Guinea','Angola','Chad','Comoros','Argentina','Honduras','Italy',
        'Cambodia','Haiti','India','Bahrain','Bhutan','Cuba','El Salvador','Hungary',
        'Iran, Islamic Rep.',"Korea, Dem. People's Rep.",'Algeria'
    ]
    years = list(range(1990, 2024, 3))
    chart_data = []
    for cn in selected:
        if cn not in pts:
            continue
        vals = [round(pts[cn][yr], 0) if yr in pts[cn] else None for yr in years]
        start = pts[cn].get(1990)
        end = pts[cn].get(2023)
        if start is None or end is None:
            continue
        chart_data.append({
            "n": cn,
            "s": vals,
            "e": round(start, 0),
            "l": round(end, 0),
            "y0": 1990,
            "step": 3
        })

    print(f"Final dataset: {len(chart_data)} countries")
    for row in chart_data:
        print(f"  {row['n']}: {row['e']}% -> {row['l']}% ({row['l']-row['e']:+.0f}pp)")
    return chart_data, selected, years


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — shows many trend lines compactly
        - **Country selection**: 8 lowest-coverage countries, 4 big fallers, 4 big risers, 7 high achievers
        - **Time range**: 1990–2023, sampled every 3 years (12 data points per cell)
        - **Color**: Red/orange = fell or low; green = improved strongly
        - **Highlights**: Central African Republic fell from 82% to 39%; Italy rose from 43% to 95%
        """
    )
    return


@app.cell
def _(chart_data, json):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
