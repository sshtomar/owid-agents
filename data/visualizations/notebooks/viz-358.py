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
        # Nuclear Electricity Share — Methodology

        Slope chart comparing % of electricity from nuclear sources in 1990 vs 2022,
        from World Bank indicator EG.ELC.NUCL.ZS. Shows who expanded, who phased out.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-NUCL-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    selected = ['France','Belgium','Korea, Rep.','Hungary','Finland','Bulgaria',
                'Germany','Japan','Czechia','Canada','Argentina','China']

    by_country = {}
    for r in data:
        c = r["countryName"]
        if c in selected and r["value"] is not None:
            if c not in by_country:
                by_country[c] = {}
            by_country[c][r["year"]] = r["value"]

    def get_nearest(yrs, target):
        for off in [0, -1, 1, -2, 2]:
            if target + off in yrs:
                return round(yrs[target + off], 2)
        return None

    chart_data = []
    for c in selected:
        if c not in by_country:
            continue
        yrs = by_country[c]
        a = get_nearest(yrs, 1990)
        b = get_nearest(yrs, 2022)
        if a is not None and b is not None:
            chart_data.append({"n": c, "a": a, "b": b})
            print(f"{c}: {a:.1f}% → {b:.1f}% ({b-a:+.1f}pp)")
    return by_country, chart_data, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — compares two time points across many countries
        - **Time points**: 1990 (pre-Fukushima, pre-phaseout era) vs 2022 (latest full year)
        - **Colors**: Green = growing share, amber = stable, red/terra = declining
        - **Highlights**: Germany fell 27%→6% (phaseout); Czechia rose 20%→37%; France still dominant at 62%
        """
    )
    return


if __name__ == "__main__":
    app.run()
