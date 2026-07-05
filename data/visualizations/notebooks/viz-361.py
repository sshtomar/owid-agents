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
        # Breast Cancer 5-Year Survival Rate, 2021 — Methodology

        This notebook documents the data pipeline behind viz-361.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--CANCERSURVIVAL_BREASTCANCER.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = {
        'SWE': 'Sweden', 'MCO': 'Monaco', 'JPN': 'Japan', 'FIN': 'Finland',
        'CYP': 'Cyprus', 'DNK': 'Denmark', 'BEL': 'Belgium', 'AUS': 'Australia',
        'USA': 'USA', 'ISR': 'Israel', 'BRA': 'Brazil',
        'KOR': 'South Korea', 'ARG': 'Argentina', 'MEX': 'Mexico',
        'CHL': 'Chile', 'CHN': 'China', 'THA': 'Thailand',
        'IND': 'India', 'EGY': 'Egypt', 'ZAF': 'South Africa',
        'GHA': 'Ghana', 'KEN': 'Kenya', 'ETH': 'Ethiopia',
        'SWZ': 'Eswatini', 'SOM': 'Somalia', 'NGA': 'Nigeria',
        'LSO': 'Lesotho', 'CAF': 'Cent. African Rep.'
    }

    chart_data = []
    for row in data:
        code = row['country']
        if code in selected:
            chart_data.append({'n': selected[code], 'v': round(row['value'], 1)})

    chart_data.sort(key=lambda x: x['v'], reverse=True)
    print(f"Countries: {len(chart_data)}")
    vals = [x['v'] for x in chart_data]
    print(f"Range: {min(vals):.1f}% – {max(vals):.1f}%")
    print(f"Gap (top minus bottom): {max(vals) - min(vals):.1f}pp")
    return chart_data, selected, vals


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Horizontal bar chart — ranked snapshot, single year
        - **Country selection**: 28 countries spanning all income levels and regions
        - **Year**: 2021 (only available year in this dataset)
        - **Highlights**: Monaco/Sweden at 92–94% vs. Central African Republic at 24.6%; a 70pp gap explained largely by late-stage diagnosis and treatment access in low-income countries
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(',', ':')))
    return


if __name__ == "__main__":
    app.run()
