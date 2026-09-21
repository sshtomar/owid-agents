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
        # Human Capital Index 2020 -- Methodology

        Horizontal bar chart of HCI values for 30 countries across income levels.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--HD-HCI-OVRL.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    # Select 30 representative countries, 2020 values
    target_names = [
        'Singapore', 'Japan', 'Korea, Rep.', 'Canada', 'Finland', 'Sweden', 'Ireland',
        'Netherlands', 'United Kingdom', 'Germany', 'France', 'United States', 'Australia',
        'Poland', 'China', 'Brazil', 'Mexico', 'Colombia', 'South Africa', 'Iran, Islamic Rep.',
        'Indonesia', 'India', 'Nigeria', 'Pakistan', 'Ethiopia', 'Bangladesh', 'Mozambique',
        'Chad', 'Mali', 'Central African Republic'
    ]
    chart_data = []
    for pt in data:
        cn = pt.get('countryName', '')
        if cn in target_names and pt['year'] == 2020 and pt['value'] is not None:
            chart_data.append({'n': cn, 'v': round(pt['value'], 3)})
    chart_data.sort(key=lambda x: x['v'])
    print(f"Countries selected: {len(chart_data)}")
    for c in chart_data:
        print(f"  {c['n']}: {c['v']}")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart sorted lowest to highest — immediately shows ranking
        - **Color**: Encodes value band (green=high, amber=medium, red=low)
        - **Country selection**: 30 countries spanning all income deciles across 6 continents
        - **Story**: Singapore's 0.879 score vs Chad's 0.30 shows a 3x gap in human capital productivity;
          Asian economies dominate the top; Sub-Saharan Africa clustered at the bottom
        """
    )
    return


if __name__ == "__main__":
    app.run()
