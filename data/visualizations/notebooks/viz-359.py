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
        # Urban Population Growth Rate -- Methodology

        Trend lines showing annual urban population growth (%) for 10 countries,
        1970-2023. Captures countries at different stages of the urbanization
        transition: rapidly urbanizing Africa/South Asia vs. post-urban-transition
        East Asia and Europe.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-URB-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['China', 'India', 'Ethiopia', 'Congo, Dem. Rep.', 'Bangladesh',
                'Brazil', 'Korea, Rep.', 'Japan', 'Germany', 'Argentina']
    display_names = {'Congo, Dem. Rep.': 'DR Congo', 'Korea, Rep.': 'Korea'}
    by_country = {}
    for row in data:
        if row['value'] is None:
            continue
        n = row['countryName']
        if n not in by_country:
            by_country[n] = {}
        by_country[n][row['year']] = row['value']

    chart_data = []
    for name in selected:
        if name not in by_country:
            continue
        pts = [{'y': y, 'v': round(by_country[name][y], 2)}
               for y in sorted(by_country[name]) if 1970 <= y <= 2023]
        last = pts[-1]['v'] if pts else 0
        chart_data.append({'n': display_names.get(name, name), 'pts': pts, 'last': last})

    chart_data.sort(key=lambda x: -x['last'])
    print(f"Countries by recent rate: {[(d['n'], d['last']) for d in chart_data]}")
    return by_country, chart_data


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — reveals long-run urbanization trajectories
        - **Country selection**: Three groups — fast urbanizing, mid, near-complete
        - **Time range**: 1970-2023 (full post-industrial era)
        - **Highlights**: Bangladesh peaked at 12% in 1970s; China peaked ~1984;
          DR Congo and Ethiopia sustain 4%+ today; Korea and Japan near zero/negative
        """
    )
    return


if __name__ == "__main__":
    app.run()
