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
        # Population Growth Rate (Annual %), 1961–2024 — Methodology

        Sparkline grid showing how population growth has converged downward
        across countries and regions over six decades.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-POP-GROW.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    key_countries = [
        'Kenya', 'Ethiopia', 'Sub-Saharan Africa',
        'India', 'Indonesia', 'South Asia',
        'Iran, Islamic Rep.', 'Brazil', 'World',
        'China', 'Japan', 'Germany',
        'Korea, Rep.', 'Europe & Central Asia',
    ]
    name_map = {
        'Iran, Islamic Rep.': 'Iran',
        'Korea, Rep.': 'South Korea',
        'Sub-Saharan Africa': 'Sub-Saharan Af.',
        'Europe & Central Asia': 'Europe & C. Asia',
    }
    cdata = {}
    for pt in data:
        name = pt['countryName']
        year = pt['year']
        val = pt['value']
        if val is not None and name in key_countries:
            if name not in cdata:
                cdata[name] = {}
            cdata[name][year] = round(val, 2)

    print("Growth rate summary:")
    for name in key_countries:
        if name in cdata:
            vals = list(cdata[name].values())
            print(f"  {name}: {min(vals):.2f}% to {max(vals):.2f}%, latest={cdata[name].get(2023, 'N/A')}")
    return cdata, key_countries, name_map


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Sparkline grid — compact multi-entity comparison of 14 countries/regions
        - **Country selection**: Ordered from high-growth (Sub-Saharan Africa, Ethiopia, Kenya) to
          converging (India, Indonesia, Brazil, Iran) to negative (China, Japan, Germany)
        - **Time range**: 1961–2024 — full post-war data capturing the demographic transition
        - **Layout**: 4 columns × 4 rows, sorted roughly by 2024 growth rate (high → low)
        - **Highlights**: China crossed into negative growth (2022), Japan has been negative since 2008
          Kenya peaked at 3.99% (1966) and has halved to ~2%; Iran shows a dramatic spike in 1980-81
        """
    )
    return


@app.cell
def _(json, cdata, key_countries, name_map):
    series = []
    for name in key_countries:
        if name in cdata:
            ydata = cdata[name]
            pts = [round(ydata[yr], 2) for yr in range(1961, 2025) if yr in ydata]
            if pts:
                short = name_map.get(name, name)
                latest = ydata.get(2023) or ydata.get(2022) or list(ydata.values())[-1]
                earliest = ydata.get(1961) or list(ydata.values())[0]
                series.append({'n': short, 's': pts, 'y0': 1961, 'e': round(earliest, 2), 'l': round(latest, 2)})
    print(json.dumps(series, separators=(',', ':')))
    return (series,)


if __name__ == "__main__":
    app.run()
