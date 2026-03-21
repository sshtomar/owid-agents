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
        # Bottoms Up

        Alcohol consumption per capita (litres pure alcohol per year, ages 15+) for 25 countries. Horizontal bar chart colored by consumption level, from Czech Republic's 12.85L to Iran's 0.0L.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol), by beverage type** (WHO Global Health Observatory)  
  Alcohol, recorded per capita (15+) consumption (in litres of pure alcohol), by beverage type from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/SA_0000001400](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/SA_0000001400)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--SA_0000001400.json"
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

        - Czech Republic leads at 12.85 litres per capita, followed closely by France (12.6) and Ireland (12.51)
        - Russia at 7.03L is lower than many Western European countries, reflecting anti-alcohol campaigns
        - Muslim-majority countries (Iran, Pakistan, Indonesia) cluster near zero
        - India reports just 0.002L per capita, likely reflecting underreporting and large abstinent populations
        """
    )
    return


if __name__ == "__main__":
    app.run()
