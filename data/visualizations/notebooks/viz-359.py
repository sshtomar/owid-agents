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
        # DPT Immunization Coverage by Region — Methodology

        Trend lines for five world regions, 1980–2024.
        Shows the global vaccination success story.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-IMM-IDPT.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data, json):
    target_regions = ['Sub-Saharan Africa', 'South Asia', 'East Asia & Pacific',
                      'Latin America & Caribbean', 'World']
    regions = {}
    for pt in data:
        c = pt['countryName']
        if c in target_regions and pt['value'] is not None:
            if c not in regions:
                regions[c] = {}
            regions[c][pt['year']] = pt['value']

    chart_data = []
    for c in target_regions:
        if c in regions:
            pts = sorted(regions[c].items())
            s = [round(v, 0) for y, v in pts]
            chart_data.append({"n": c, "s": s, "y0": pts[0][0], "step": 1})

    print(f"Chart data: {len(chart_data)} regions")
    for item in chart_data:
        print(f"  {item['n']}: {item['y0']}-{item['y0']+len(item['s'])-1}, first={item['s'][0]}, latest={item['s'][-1]}")
    print(json.dumps(chart_data, separators=(',', ':')))
    return (chart_data, regions, target_regions)


if __name__ == "__main__":
    app.run()
