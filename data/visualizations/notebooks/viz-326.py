import marimo

__generated_with = "0.13.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Renewable Electricity Output (% of total)

        **Dataset**: World Bank - EG.ELC.RNEW.ZS
        **Viz ID**: viz-326

        Renewable electricity output as a share of total electricity output,
        for selected countries with interesting energy transition stories.
        """
    )
    return


@app.cell
def _():
    import json
    return (json,)


@app.cell
def _(json, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-RNEW-ZS.json"
    with open(str(_path)) as _f:
        raw = json.load(_f)
    return (raw,)


@app.cell
def _(raw):
    targets = [
        "Denmark", "Germany", "China", "India",
        "Brazil", "Kenya", "Australia", "Japan",
    ]
    filtered = [d for d in raw["data"] if d["countryName"] in targets and d["value"] is not None]
    print(f"Total records after filtering: {len(filtered)}")
    print(f"Countries: {sorted(set(d['countryName'] for d in filtered))}")
    print(f"Year range: {min(d['year'] for d in filtered)} - {max(d['year'] for d in filtered)}")
    return filtered, targets


@app.cell
def _(filtered, mo, targets):
    # Summary stats per country: latest value and change from earliest to latest
    _rows = []
    for _country in targets:
        _vals = sorted(
            [d for d in filtered if d["countryName"] == _country],
            key=lambda d: d["year"],
        )
        if _vals:
            _first = _vals[0]
            _last = _vals[-1]
            _change = round(_last["value"] - _first["value"], 1)
            _rows.append(
                f"| {_country} | {_first['year']} | {round(_first['value'], 1)}% "
                f"| {_last['year']} | {round(_last['value'], 1)}% | {'+' if _change >= 0 else ''}{_change}pp |"
            )

    mo.md(
        "## Summary Statistics\n\n"
        "| Country | First Year | First Value | Last Year | Last Value | Change |\n"
        "|---------|-----------|-------------|----------|-----------|--------|\n"
        + "\n".join(_rows)
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        **Chart type**: Line chart showing renewable electricity as % of total output over time.

        **Key stories in the data**:

        - **Brazil** has always been high (around 80-95%) due to extensive hydropower infrastructure.
        - **Kenya** similarly high historically, relying on geothermal and hydro, though volatile.
        - **Denmark** shows the most dramatic transition: from ~3% in 1990 to ~79% in 2021,
          driven primarily by wind energy investment.
        - **Germany** shows rapid recent growth from ~4% to ~40%, reflecting the Energiewende policy.
        - **China** and **India** are rising from a low base, reaching ~28% and ~19% respectively.
        - **Japan** and **Australia** show moderate but accelerating growth in recent years.

        Note: United States and United Kingdom had no data in this World Bank indicator,
        so the visualization focuses on 8 countries with complete data.
        """
    )
    return


@app.cell
def _(filtered, json):
    chart_data = [
        {"n": d["countryName"], "y": d["year"], "v": round(d["value"] * 10) / 10}
        for d in filtered
    ]
    chart_data.sort(key=lambda d: (d["y"], -d["v"]))
    print(json.dumps(chart_data))
    return (chart_data,)


if __name__ == "__main__":
    app.run()
