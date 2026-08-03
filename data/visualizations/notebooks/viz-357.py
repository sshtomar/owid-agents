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
        # Central Government Debt, 1990-2023 -- Methodology

        Sparkline grid showing government debt (% of GDP) trajectories for 21
        countries with at least 15 years of data. Sorted by most recent value.
        Forward-fills gaps in data to show continuous trend lines.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--GC-DOD-TOTL-GD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    exclude_words = ['income', 'OECD', 'Euro ', 'Europe', 'Asia', 'Africa', 'America',
                     'Caribbean', 'East ', 'South Asia', 'West ', 'North America',
                     'Pacific', 'Global', 'IDA', 'IBRD', 'Post-', 'Pre-', 'Late-',
                     'Early-', 'Fragile', 'Small', 'Landlocked', 'countries',
                     'Developing', 'states', 'dividend', 'members', 'Arab', 'Council',
                     'Organisation', 'World']
    by_country = {}
    for row in data:
        name = row['countryName']
        year = row['year']
        val = row['value']
        if val is None:
            continue
        if any(x in name for x in exclude_words):
            continue
        if name not in by_country:
            by_country[name] = {}
        by_country[name][year] = val
    good = sorted([(n, yrs) for n, yrs in by_country.items() if len(yrs) >= 15],
                  key=lambda x: -len(x[1]))[:24]
    print(f"Countries with 15+ years of data: {len(good)}")
    return by_country, good


@app.cell
def _(good):
    y0 = 1990
    chart_data = []
    for name, yrs in good:
        s = [round(yrs.get(y), 1) if yrs.get(y) is not None else None for y in range(y0, 2024)]
        filled = list(s)
        for i in range(1, len(filled)):
            if filled[i] is None and filled[i-1] is not None:
                filled[i] = filled[i-1]
        filled = [v if v is not None else 0 for v in filled]
        first_yr = min(yr for yr in yrs if yr >= y0)
        last_yr = max(yr for yr in yrs if yr >= y0)
        chart_data.append({"n": name, "s": filled, "e": round(yrs[first_yr], 1),
                            "l": round(yrs[last_yr], 1), "y0": y0})
    chart_data.sort(key=lambda x: -x["l"])
    print(f"Chart data: {len(chart_data)} countries")
    print(f"Top 3: {[(d['n'], d['l']) for d in chart_data[:3]]}")
    return chart_data, y0


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — many entities, one trajectory each
        - **Country selection**: 21 countries with 15+ years of complete data
        - **Time range**: 1990-2023 (forward-filling sparse years)
        - **Highlights**: Bahrain and El Salvador show steep post-2010 rises;
          Jamaica reduced from 140%+ to ~98%; Korea went from 7% to 49%
        """
    )
    return


if __name__ == "__main__":
    app.run()
