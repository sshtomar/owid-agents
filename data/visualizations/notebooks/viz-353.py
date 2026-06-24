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
        # Old-Age Dependency Ratio Trend Lines -- Methodology

        Shows the number of people aged 65+ per 100 working-age people (15-64) from 1960
        to 2023 for 8 countries spanning the spectrum from rapidly aging (Japan, South Korea)
        to still-young populations (India, Brazil).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-DPND-OL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    targets = ['Japan', 'Korea, Rep.', 'Italy', 'Germany', 'Finland', 'China', 'Brazil', 'India']
    country_ts = {}
    for x in data:
        n = x['countryName']
        if n in targets and x['value'] is not None:
            if n not in country_ts:
                country_ts[n] = {}
            country_ts[n][x['year']] = x['value']

    for c in targets:
        if c in country_ts:
            ts = country_ts[c]
            print(f"{c}: {ts.get(1960, '?')} -> {ts.get(2023, '?')}")
    return country_ts, targets


@app.cell
def _(json, country_ts, targets):
    years_sample = list(range(1960, 2025, 3))
    name_map = {'Korea, Rep.': 'South Korea'}
    chart_data = []
    for n in targets:
        if n not in country_ts:
            continue
        ts = country_ts[n]
        pts = []
        for y in years_sample:
            if y in ts:
                pts.append({"y": y, "v": round(ts[y], 1)})
        if pts:
            chart_data.append({"n": name_map.get(n, n), "pts": pts})

    print(json.dumps(chart_data, separators=(',', ':')))
    return chart_data, name_map, years_sample


if __name__ == "__main__":
    app.run()
