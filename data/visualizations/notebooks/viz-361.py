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
        # Average Annual Precipitation -- Methodology

        Horizontal bar chart showing 25 countries from driest to wettest.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-LND-PRCP-MM.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    skip_words = ['&', 'income', 'world', 'region', 'Europe', 'Asia', 'Africa',
                  'Pacific', 'America', 'Caribbean', 'IBRD', 'IDA', 'OECD',
                  'states', 'dividend', 'countries', 'total', 'Fragile']
    by_country = {}
    for pt in data:
        cn = pt.get('countryName', '')
        yr = pt['year']
        val = pt.get('value')
        if val is not None and cn and not any(w.lower() in cn.lower() for w in skip_words) and yr >= 1990:
            if cn not in by_country:
                by_country[cn] = []
            by_country[cn].append(val)

    # Long-run average
    avg = {cn: round(sum(v)/len(v), 0) for cn, v in by_country.items() if len(v) >= 5}
    sorted_all = sorted(avg.items(), key=lambda x: x[1])

    # Select 25 diverse countries
    notable = {'Egypt, Arab Rep.': 'Egypt', 'Saudi Arabia': 'Saudi Arabia',
               'Australia': 'Australia', 'India': 'India', 'United States': 'United States',
               'China': 'China', 'Brazil': 'Brazil', 'United Kingdom': 'United Kingdom',
               'Germany': 'Germany', 'Japan': 'Japan', 'Nigeria': 'Nigeria',
               'Indonesia': 'Indonesia', 'Colombia': 'Colombia', 'Bangladesh': 'Bangladesh',
               'Norway': 'Norway', 'Czechia': 'Czechia', 'Iran, Islamic Rep.': 'Iran',
               'Brunei Darussalam': 'Brunei', 'Costa Rica': 'Costa Rica',
               'Antigua and Barbuda': 'Antigua & Barbuda', 'Dominican Republic': 'Dominican Rep.',
               'Cameroon': 'Cameroon', 'Bolivia': 'Bolivia', 'Argentina': 'Argentina',
               'Azerbaijan': 'Azerbaijan', 'Jordan': 'Jordan', 'Bahrain': 'Bahrain',
               'Algeria': 'Algeria', 'Iraq': 'Iraq', 'Belgium': 'Belgium'}

    chart_data = []
    seen = set()
    for cn, v in sorted_all:
        label = notable.get(cn, cn)
        if label not in seen and len(chart_data) < 25:
            chart_data.append({'n': label, 'v': int(v)})
            seen.add(label)

    chart_data.sort(key=lambda x: x['v'])
    print(f"Final: {len(chart_data)} countries")
    for c in chart_data:
        print(f"  {c['n']}: {c['v']} mm")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart sorted driest to wettest — precipitation is a natural ordering
        - **Color**: Warm tones for dry, cool blue for wet climates
        - **Story**: Egypt's 18 mm vs Colombia's 3,230 mm is a 180x difference; illustrates why water security is existential in some regions
        """
    )
    return


if __name__ == "__main__":
    app.run()
