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
        # Youth Labor Force Participation Rate — Methodology

        Sparkline grid showing 1990–2024 trends for 29 countries. Sorted by
        latest participation rate to reveal the high–low geography clearly.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-ACTI-1524-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    aggregate_patterns = [
        'income', 'World', '& Pacific', '& Central', 'Middle East',
        'Latin America', 'Sub-Saharan', 'North Africa', 'Euro area', 'South Asia',
        'East Asia', 'Arab World', 'Caribbean small', 'OECD', 'fragile', 'Fragility',
        'IDA', 'IBRD', 'island', 'Small states', 'Heavily', 'Least',
        'demographic', 'Africa Western', 'Africa Eastern', 'Europe &',
        'North America', 'European Union', 'Central Europe'
    ]
    def is_agg(cn):
        return any(x.lower() in cn.lower() for x in aggregate_patterns)

    countries = {}
    for row in data:
        cn = row['countryName']
        if row['value'] is None or is_agg(cn):
            continue
        if cn not in countries:
            countries[cn] = {}
        countries[cn][row['year']] = round(row['value'], 1)

    selected = [
        'Iceland', 'Australia', 'Denmark', 'Canada', 'Austria', 'Germany',
        'Brazil', 'Bolivia', 'Colombia', 'France', 'Ireland', 'Japan',
        'Bangladesh', 'China', 'Indonesia', 'India', 'Kenya', 'Ethiopia',
        'Algeria', 'Egypt, Arab Rep.', 'Greece', 'Iran, Islamic Rep.', 'Italy', 'Jordan',
        'Korea, Rep.', 'Bulgaria', 'Djibouti', 'Chile', 'Afghanistan'
    ]
    result = []
    for cn in selected:
        if cn not in countries:
            continue
        ydata = countries[cn]
        pts = sorted((y, v) for y, v in ydata.items() if 1990 <= y <= 2024)
        if len(pts) < 20:
            continue
        s = [v for _, v in pts]
        label = cn.replace(', Arab Rep.', '').replace(', Rep.', '').replace(', Islamic Rep.', '')
        result.append({'n': label, 's': s, 'e': round(s[0], 1), 'l': round(s[-1], 1), 'y0': pts[0][0]})

    print(f"Countries: {len(result)}")
    for r in result:
        print(f"  {r['n']}: {r['e']}% → {r['l']}%")
    return countries, is_agg, result, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — compact overview of 29 country trajectories
        - **Sorting**: By latest participation rate (descending), highest top-left
        - **Highlights**: China fell from 78% to 50% as education expanded; Iceland rose to 82%; Djibouti at 13.5%
        - **5 columns**: Natural fit for 29 countries in a readable grid
        """
    )
    return


@app.cell
def _(json, result):
    result_sorted = sorted(result, key=lambda x: -x['l'])
    print(json.dumps(result_sorted, separators=(",", ":")))
    return (result_sorted,)


if __name__ == "__main__":
    app.run()
