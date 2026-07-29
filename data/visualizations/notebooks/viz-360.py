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
        # Battle-Related Deaths — Methodology

        Trend lines for 6 countries showing annual battle-related deaths from 1989 to 2024.
        Captures Afghanistan's sustained conflict, Iraq's two surges, Ethiopia's Tigray war,
        and the Israel-Gaza escalation in 2023.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--VC-BTL-DETH.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data):
    countries = {}
    for p in data:
        c = p["countryName"]
        if p["value"] is not None:
            if c not in countries:
                countries[c] = {}
            countries[c][p["year"]] = p["value"]
    return (countries,)


@app.cell
def _(countries):
    chosen = ["Afghanistan", "Ethiopia", "Iraq", "Israel", "Congo, Dem. Rep.", "India"]
    chart_data = []
    for name in chosen:
        if name not in countries:
            continue
        vals = countries[name]
        series = []
        for yr in range(1989, 2025):
            v = vals.get(yr, 0)
            series.append(int(v))
        total = sum(series)
        peak = max(series)
        peak_yr = 1989 + series.index(peak)
        chart_data.append({"n": name, "s": series, "total": total, "peak": peak, "peak_yr": peak_yr})

    print("Summary:")
    for d in chart_data:
        print(f"  {d['n']}: total={d['total']:,}, peak={d['peak']:,} in {d['peak_yr']}")
    return (chart_data,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — shows outbreak timing and duration of conflict episodes
        - **Year range**: 1989–2024 (full post-Cold War era)
        - **Country selection**: Countries with the largest cumulative or most notable peak deaths
        - **Cap**: Y-axis capped at 35,000 for readability; Ethiopia's 2022 peak (~125k) is clipped
        - **Highlights**: Afghanistan sustained conflict 1989-2021; Ethiopia Tigray war 2020-2022;
          Iraq Gulf War 1991 and ISIS 2014-2017 peaks; Israel 2023 Gaza escalation
        """
    )
    return


@app.cell
def _(json, chart_data):
    export = [{"n": d["n"], "s": d["s"]} for d in chart_data]
    print(json.dumps(export, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
