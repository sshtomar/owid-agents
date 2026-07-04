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
        # R&D Researchers per Million People -- Methodology

        Trend lines for 10 countries showing researchers in R&D (full-time equivalent)
        per million people, 2000-2023. Korea's dramatic rise from 2,324 to 9,472 is the
        central story. China grew from 550 to 2,107 -- still far below the leaders.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-SCIE-RD-P6.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    target = ['Korea, Rep.', 'Denmark', 'Finland', 'Austria', 'Germany', 'Japan', 'France', 'China', 'Canada', 'Belgium']
    by_cy = {}
    for row in data:
        c = row['countryName']
        y = row['year']
        v = row['value']
        if v is not None and c in target:
            if c not in by_cy:
                by_cy[c] = {}
            by_cy[c][y] = round(v, 0)
    for c in target:
        if c in by_cy:
            years = sorted(by_cy[c].keys())
            print(f"{c}: {years[0]}-{years[-1]}, latest={by_cy[c][max(years)]:.0f}")
    return by_cy, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows diverging trajectories over 23 years
        - **Country selection**: Top 10 by 2023 value among countries with long series
        - **Highlights**: Korea overtook Japan in 2010, now 70% higher; China tripling since 2000
        - **Note**: US not in dataset (does not report to World Bank on this indicator)
        """
    )
    return


@app.cell
def _(json, by_cy, target):
    chart_data = []
    for c in target:
        if c in by_cy:
            years = sorted(by_cy[c].keys())
            pts = [{"y": yr, "v": by_cy[c][yr]} for yr in years if 2000 <= yr <= 2024]
            chart_data.append({"n": c, "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
