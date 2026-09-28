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
        # China's Rise to Dominate Global Patent Filings -- Methodology

        Trend lines chart showing patent applications by residents for 6 countries
        from 1995 to 2021. Uses World Bank indicator IP.PAT.RESD (sourced from WIPO).
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IP-PAT-RESD.json"
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
    target = ['China', 'Japan', 'Korea, Rep.', 'Germany', 'India', 'France']
    by_country = defaultdict(dict)
    for x in filtered:
        if x['countryName'] in target:
            by_country[x['countryName']][x['year']] = int(x['value'])

    print("Patent applications (1995 vs 2021):")
    for c in target:
        if c not in by_country:
            continue
        years = sorted(by_country[c].keys())
        v1995 = by_country[c].get(1995, by_country[c][years[0]])
        vlast = by_country[c][years[-1]]
        growth = vlast / v1995
        print(f"  {c}: {v1995:,} -> {vlast:,} ({growth:.1f}x)")
    return by_country, target


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines -- China's exponential trajectory is best shown as a
          continuous time series to emphasize the acceleration.
        - **Country selection**: Top 5 patent filers outside the US (US data unavailable in
          this dataset). China, Japan, Korea represent East Asia's innovation ecosystem;
          Germany and France represent Europe; India shows emerging market trajectory.
        - **Time range**: 1995-2021 (26 years). China's rise starts around 2000 and becomes
          dramatic after 2008.
        - **Annotation**: Mark 2011 when China passed Japan as the clearest inflection point.
        - **Highlights**: China grew 142x (10k to 1.4M); Japan fell from 387k to 222k;
          India grew 17x but from a small base. Korea grew 3x. This chart shows the most
          dramatic shift in the global innovation landscape in modern history.
        """
    )
    return


@app.cell
def _(json, by_country, target):
    chart_data = []
    for c in target:
        if c not in by_country:
            continue
        filtered_c = {y: v for y, v in by_country[c].items() if y >= 1995}
        years = sorted(filtered_c.keys())
        vals = [filtered_c[y] for y in years]
        chart_data.append({"n": c, "y0": years[0], "s": vals})
    print(json.dumps(chart_data, separators=(",", ":")))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
