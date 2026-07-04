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
        # Learning Poverty: Children Below Minimum Reading Proficiency -- Methodology

        This notebook documents the data pipeline for the learning poverty bar chart.
        The World Bank Learning Poverty indicator (SE.LPV.PRIM) combines two dimensions:
        children who are in school but read below minimum proficiency PLUS children who
        are out of school entirely.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SE-LPV-PRIM.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    skip_kw = ('Africa', 'East', 'Europe', 'Latin', 'Middle', 'North', 'South', 'Sub', 'World', 'High', 'Low', 'Lower', 'Upper', 'Least', 'Fragile', 'Small', 'IBRD', 'IDA', 'OECD', 'Arab', 'Central', 'Pacific', 'Caribbean', 'Heavily', 'income', 'dividend', 'region', 'members', 'countries', 'states', 'Eurasia', 'Asia', 'America', 'Euro')
    by_country = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is not None and not any(k.lower() in c.lower() for k in skip_kw):
            if c not in by_country or y > by_country[c][1]:
                by_country[c] = (v, y)
    recent = [(c, v, y) for c, (v, y) in by_country.items() if y >= 2015]
    recent.sort(key=lambda x: x[1], reverse=True)
    print(f"Countries with 2015+ data: {len(recent)}")
    print(f"Range: {min(v for _,v,_ in recent):.1f}% - {max(v for _,v,_ in recent):.1f}%")
    return by_country, recent


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart -- best for comparing many countries ranked by a single value
        - **Country selection**: All 55 countries with data from 2015 or later (reduces staleness)
        - **Color encoding**: Red ≥70%, orange 50-70%, amber 30-50%, sage 15-30%, green <15%
        - **Story**: Congo DRC, Burundi, Chad have >90% learning poverty; Korea, Ireland are at ~2-3%
        """
    )
    return


@app.cell
def _(json, recent):
    chart_data = [{"n": c, "v": round(v, 1), "y": y} for c, v, y in recent]
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
