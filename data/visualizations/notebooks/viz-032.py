import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Left Behind

        Out-of-school rate for primary education, earliest vs most recent year, for 15 countries. Slope chart showing dramatic improvements in Sub-Saharan Africa and South Asia, with South Sudan as the only country that worsened.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Out-of-School Rate, Primary (%)** (unesco)  
  Out-of-School Rate, Primary (%) from unesco  
  Source: [https://data.uis.unesco.org/](https://data.uis.unesco.org/)
        """
    )
    return


@app.cell
def _():
    import json
    import urllib.request
    import pandas as pd
    import altair as alt
    return json, urllib, pd, alt


@app.cell
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "unesco--ROFST-1-CP.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_0 = _raw["meta"]
    df_0 = pd.DataFrame(_raw["data"])
    df_0 = df_0.dropna(subset=["value"])
    mo.md(f"**{meta_0['title']}** -- {len(df_0)} rows, {df_0['countryName'].nunique()} countries, {df_0['year'].min()}--{df_0['year'].max()}")
    mo.ui.table(df_0.head(20))
    return (df_0, meta_0)


@app.cell
def _(mo):
    mo.md(
        """
        ## Transformation

        For a before/after view we take the earliest and latest observation per country and compute the change over time.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _earliest = df_0.loc[df_0.groupby("countryName")["year"].idxmin()][["countryName", "year", "value"]]
    _earliest.columns = ["countryName", "start_year", "start_value"]
    _latest = df_0.loc[df_0.groupby("countryName")["year"].idxmax()][["countryName", "year", "value"]]
    _latest.columns = ["countryName", "end_year", "end_value"]
    _merged = _earliest.merge(_latest, on="countryName")
    _merged["delta"] = _merged["end_value"] - _merged["start_value"]
    transformed = _merged.sort_values("delta", ascending=False).head(20).copy()
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, pd, mo):
    _start = transformed[["countryName", "start_year", "start_value"]].rename(
        columns={"start_year": "year", "start_value": "value"}
    )
    _start["period"] = "start"
    _end = transformed[["countryName", "end_year", "end_value"]].rename(
        columns={"end_year": "year", "end_value": "value"}
    )
    _end["period"] = "end"
    _plot_df = pd.concat([_start, _end], ignore_index=True)

    _lines = (
        alt.Chart(_plot_df)
        .mark_line()
        .encode(
            x=alt.X("period:N", title="Period", sort=["start", "end"]),
            y=alt.Y("value:Q", title="Value"),
            detail="countryName:N",
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "period", "value"],
        )
    )
    _points = (
        alt.Chart(_plot_df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("period:N", sort=["start", "end"]),
            y=alt.Y("value:Q"),
            color=alt.Color("countryName:N"),
            tooltip=["countryName", "period", "year", "value"],
        )
    )
    _chart = (_lines + _points).properties(width=500, height=400)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Guinea reduced its out-of-school rate from 75.8% to 14.7%, one of the largest improvements
        - India went from 23.4% to just 0.1%, essentially achieving universal primary enrollment
        - Mozambique dropped from 51.7% to 1.0%, an extraordinary transformation
        - South Sudan is the only country shown where the rate worsened, from 55.3% to 64.7%
        """
    )
    return


if __name__ == "__main__":
    app.run()
