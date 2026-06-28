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
        # Youth NEET Rate Trend Lines -- Methodology

        NEET = Not in Education, Employment, or Training.
        Tracks the share of young people aged 15-24 outside all three
        mainstream paths for human capital development.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-UEM-NEET-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    from collections import defaultdict

    selected = {
        'IN': 'India', 'IR': 'Iran', 'AL': 'Albania', 'BA': 'Bosnia',
        'ID': 'Indonesia', 'CO': 'Colombia', 'EC': 'Ecuador', 'CL': 'Chile',
        'FR': 'France', 'CA': 'Canada', 'HN': 'Honduras',
    }

    by_country = defaultdict(list)
    for x in data:
        if x['country'] in selected and x['year'] >= 2000 and x['value'] is not None:
            by_country[x['country']].append((x['year'], round(x['value'], 2)))

    chart_data = []
    for cc, name in selected.items():
        pts = sorted(by_country[cc], key=lambda p: p[0])
        if pts:
            chart_data.append({'n': name, 'pts': [{'y': p[0], 'v': p[1]} for p in pts]})

    chart_data.sort(key=lambda x: -x['pts'][-1]['v'])
    print(f"Series: {len(chart_data)}")
    for s in chart_data:
        print(f"  {s['n']}: {s['pts'][0]['v']}% ({s['pts'][0]['y']}) -> {s['pts'][-1]['v']}% ({s['pts'][-1]['y']})")
    return chart_data, by_country, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines (sparkline-style) to show trajectory over 2000-2024
        - **Country selection**: Mix of high-NEET (Iran, India, Honduras, Albania, Bosnia),
          medium-NEET (Colombia, Ecuador, Indonesia), and lower-NEET (Chile, France, Canada)
        - **Color**: Improvement-band coloring based on total percentage-point decline
        - **Highlight**: India declined from ~33% to ~24%; Bosnia halved from 32% to 14%
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
