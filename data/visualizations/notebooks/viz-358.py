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
        # International Tourism Arrivals Collapse in 2020 -- Methodology

        Trend lines chart showing the COVID-19 impact on international tourism arrivals
        for 8 major destinations from 2010 to 2020. Uses World Bank indicator ST.INT.ARVL.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ST-INT-ARVL.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    filtered = [d for d in data if d["value"] is not None]
    print(f"After filtering nulls: {len(filtered)} rows")
    return (filtered,)


@app.cell
def _(filtered):
    from collections import defaultdict
    target = ['France', 'China', 'Italy', 'Japan', 'Germany', 'Greece', 'Korea, Rep.', 'Croatia']
    by_country = defaultdict(dict)
    for x in filtered:
        if x['countryName'] in target:
            by_country[x['countryName']][x['year']] = round(x['value'] / 1e6, 2)

    print("2019 vs 2020 arrivals (millions):")
    for c in target:
        if c in by_country:
            y2019 = by_country[c].get(2019)
            y2020 = by_country[c].get(2020)
            if y2019 and y2020:
                pct = (y2020 / y2019 - 1) * 100
                print(f"  {c}: {y2019:.1f}M -> {y2020:.1f}M ({pct:.0f}%)")
    return by_country, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- shows continuous trajectory for each country
          and makes the 2020 drop visually dramatic.
        - **Country selection**: Mix of established (France, Italy) and fast-growing
          destinations (Japan, Korea) with diverse COVID response severities.
        - **Time range**: 2010-2020. Starting from 2010 gives enough baseline context
          without cluttering with older data.
        - **Annotation**: Vertical dashed line + shaded region marks 2020 COVID collapse.
        - **Highlights**: Japan fell 87%, Korea 86%, China 81%; France fell only 46%.
          Island/Asia-Pacific economies closed borders completely while Europe stayed
          partially open.
        """
    )
    return


@app.cell
def _(json, by_country, target):
    chart_data = []
    for c in target:
        if c not in by_country:
            continue
        filtered_c = {y: v for y, v in by_country[c].items() if y >= 2010}
        if not filtered_c:
            continue
        years = sorted(filtered_c.keys())
        vals = [filtered_c[y] for y in years]
        chart_data.append({"n": c, "y0": years[0], "s": vals})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
