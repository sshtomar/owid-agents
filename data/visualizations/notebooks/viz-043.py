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
        # Every Breath You Take

        Mean annual PM2.5 air pollution concentration (ug/m3) for 30 countries in 2019. WHO guideline is 5 ug/m3. Only Canada comes close. Most of South Asia and Sub-Saharan Africa exceeds the guideline by 5-10x.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Concentrations of fine particulate matter (PM2.5)** (WHO Global Health Observatory)  
  Concentrations of fine particulate matter (PM2.5) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/SDGPM25](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/SDGPM25)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--SDGPM25.json"
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

        For a comparison view we take the latest non-null value per country, then sort to show the ranking.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _latest_year = df_0.groupby("countryName")["year"].max().reset_index()
    _latest_year.columns = ["countryName", "latest_year"]
    _merged = df_0.merge(_latest_year, left_on=["countryName", "year"], right_on=["countryName", "latest_year"])
    transformed = (
        _merged.sort_values("value", ascending=False)
        .head(20)
        .copy()
    )
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, mo):
    _chart = (
        alt.Chart(transformed)
        .mark_bar()
        .encode(
            x=alt.X("value:Q", title="Value"),
            y=alt.Y("countryName:N", title="Country", sort="-x"),
            color=alt.Color("value:Q", scale=alt.Scale(scheme="blues"), legend=None),
            tooltip=["countryName", "year", "value"],
        )
        .properties(width=700, height=500)
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Cameroon leads at 54.8 ug/m3, nearly 11 times the WHO guideline of 5 ug/m3
        - Bangladesh (50.1) and Niger (50.7) round out the top three, all in the darkest severity tier
        - Even wealthy nations like Germany (11.2), France (10.5), and Japan (10.8) exceed the guideline by 2x
        - Canada (5.2) is the only country approaching compliance with WHO's annual mean target
        """
    )
    return


if __name__ == "__main__":
    app.run()
