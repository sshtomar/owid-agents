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
        # The Livestock Revolution: Production Index 1961-2022 -- Methodology

        Trend lines comparing livestock production index for 8 countries over 60 years.
        The FAO/World Bank livestock production index uses 2014-2016 as baseline (=100).
        Indonesia's 14x growth and India surpassing the West are the main stories.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-PRD-LVSK-XD.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    target = ['China', 'India', 'Brazil', 'Indonesia', 'Germany', 'France', 'Argentina', 'Australia']
    by_cy = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is not None and c in target:
            if c not in by_cy:
                by_cy[c] = {}
            by_cy[c][y] = round(v, 1)
    for c in target:
        if c in by_cy:
            yrs = sorted(by_cy[c].keys())
            print(f"{c}: {by_cy[c][yrs[0]]:.1f} (1961) -> {by_cy[c][2022]:.1f} (2022)")
    return by_cy, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines 1961-2022 -- 60-year arc shows structural transformation
        - **Country selection**: 4 Global South risers + 3 Western flatliers + 1 antipodean outlier
        - **Subsample**: Every 5 years to reduce data weight while preserving shape
        - **Story**: Indonesia 190, India 133 -- both now above Western Europe at ~93
        - **Note**: Germany/France peaked ~1995 (EU CAP reforms, consumer preference shifts)
        """
    )
    return


@app.cell
def _(json, by_cy, target):
    chart_data = []
    for c in target:
        if c in by_cy:
            yrs = sorted(by_cy[c].keys())
            pts = [{"y": yr, "v": by_cy[c][yr]} for yr in yrs if 1961 <= yr <= 2022]
            chart_data.append({"n": c, "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
