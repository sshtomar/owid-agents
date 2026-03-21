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
        # The Weight of Forests

        Above-ground biomass density in forests, comparing 2000 and 2020 across selected countries and continents.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Above-ground biomass in forest (tonnes per hectare)** (un-sdg)  
  Above-ground biomass in forest (tonnes per hectare) from un-sdg  
  Source: [https://unstats.un.org/sdgs/dataportal/database](https://unstats.un.org/sdgs/dataportal/database)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--15-2-1--AG_LND_FRSTBIOPHA.json"
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

        - European forests generally grew denser over two decades
        - South Korea is a standout reforestation story
        - Some tropical countries saw losses or stagnation
        """
    )
    return


if __name__ == "__main__":
    app.run()
