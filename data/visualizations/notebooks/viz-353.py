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
        # Age Dependency Ratio — Methodology

        This notebook documents the data pipeline for the demographic transition
        trend-lines visualization showing age dependency ratios 1960–2024 for 7 countries.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    pts = [p for p in data if p['value'] is not None]
    by_country = defaultdict(dict)
    for p in pts:
        by_country[p['countryName']][p['year']] = p['value']

    focus = ['Japan', 'Germany', 'China', 'India', 'Brazil', 'Korea, Rep.', 'Ethiopia']
    name_map = {'Korea, Rep.': 'South Korea'}

    chart_data = []
    for c in focus:
        vals = by_country.get(c, {})
        step_years = list(range(1960, 2025, 5))
        pts_list = [{'y': yr, 'v': round(vals[yr], 1)} for yr in step_years if yr in vals]
        if pts_list:
            name = name_map.get(c, c)
            chart_data.append({'n': name, 'pts': pts_list})

    countries = [s['n'] for s in chart_data]
    years = [s['pts'][0]['y'] for s in chart_data]
    vals_end = [s['pts'][-1] for s in chart_data]
    print(f"Countries: {countries}")
    for s in chart_data:
        first = s['pts'][0]
        last = s['pts'][-1]
        print(f"  {s['n']}: {first['v']}% ({first['y']}) -> {last['v']}% ({last['y']})")
    return chart_data, by_country, pts


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows the full arc of demographic transition over 64 years.
        - **Country selection**: Contrasting stories: Japan (aging), South Korea (fast transition then re-rising),
          China (one-child policy effect), India (still declining), Brazil (transition complete),
          Ethiopia (still high youth dependency, slowly falling).
        - **Time range**: 1960–2024 — captures the full post-WWII demographic dividend era.
        - **Key insight**: South Korea had the fastest demographic transition on record;
          Japan's dependency ratio is now rising rapidly due to elderly, not youth.
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
