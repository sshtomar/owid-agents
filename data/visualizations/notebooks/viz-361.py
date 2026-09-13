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
        # Child Wasting Prevalence — Methodology

        Sparkline grid showing countries with highest acute malnutrition burden.
        Sorted by most recent wasting prevalence (descending).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--NUTRITION_WH_2.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    name_map = {
        'IND': 'India', 'YEM': 'Yemen', 'BFA': 'Burkina Faso', 'TJK': 'Tajikistan',
        'MRT': 'Mauritania', 'NER': 'Niger', 'DJI': 'Djibouti', 'BGD': 'Bangladesh',
        'SEN': 'Senegal', 'TLS': 'Timor-Leste', 'PAK': 'Pakistan', 'MDG': 'Madagascar',
        'TCD': 'Chad', 'PHL': 'Philippines', 'MLI': 'Mali', 'VNM': 'Vietnam',
        'COD': 'DR Congo', 'SLE': 'Sierra Leone'
    }
    target_codes = list(name_map.keys())

    countries = {}
    for pt in data:
        c = pt.get('country', '')
        if c in target_codes and pt['value'] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][pt['year']] = pt['value']

    chart_data = []
    for code in target_codes:
        if code in countries:
            pts = sorted(countries[code].items())
            if len(pts) >= 4:
                chart_data.append({
                    "n": name_map[code],
                    "s": [round(v, 1) for y, v in pts],
                    "y0": pts[0][0],
                    "e": round(pts[0][1], 1),
                    "l": round(pts[-1][1], 1),
                    "ly": pts[-1][0]
                })

    chart_data.sort(key=lambda x: -x['l'])
    print(f"Chart data: {len(chart_data)} countries")
    for item in chart_data:
        print(f"  {item['n']}: latest({item['ly']})={item['l']}%, n={len(item['s'])}")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data, countries, name_map, target_codes)


if __name__ == "__main__":
    app.run()
