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
        # Europe's Carbon Retreat

        Greenhouse gas emissions per capita (tonnes CO2 equivalent) for 15 EU countries, 1990-2024. Nordic leaders have halved their footprints while coal-dependent economies in Central Europe are still catching up.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Domestic net greenhouse gas emissions** (eurostat)  
  Domestic net greenhouse gas emissions from eurostat  
  Source: [https://ec.europa.eu/eurostat/databrowser/view/sdg_13_10/default/table](https://ec.europa.eu/eurostat/databrowser/view/sdg_13_10/default/table)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "eu--sdg_13_10.json"
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

        For a time-series view we filter to the top countries by data completeness, then plot each country as a separate line over time.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _counts = df_0.groupby("countryName").size().reset_index(name="n")
    _top = _counts.nlargest(8, "n")["countryName"]
    transformed = df_0[df_0["countryName"].isin(_top)].copy()
    transformed = transformed.sort_values(["countryName", "year"])
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, mo):
    _chart = (
        alt.Chart(transformed)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Value"),
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "year", "value"],
        )
        .properties(width=700, height=400)
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Luxembourg cut emissions from 33.4 to 11.2 tonnes per capita, a 66% reduction -- the steepest in the EU
        - Sweden has the lowest emissions at 4.5 tonnes, less than half of Germany's 7.8
        - Poland's trajectory is the flattest, declining only 27% from 12.5 to 9.1 -- still heavily dependent on coal
        - Ireland bucked the trend by rising from 13.2 to 18.3 during the Celtic Tiger boom before falling back to 10.0
        """
    )
    return


if __name__ == "__main__":
    app.run()
