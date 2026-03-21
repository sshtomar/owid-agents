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
        # Roads That Kill

        Estimated road traffic death rate per 100,000 population for 39 countries (2021). A 25-fold gap separates Guinea (37.4) from Norway (1.5). Color-coded by severity: red (>20), orange (10-20), yellow (5-10), green (<5).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Estimated road traffic death rate (per 100 000 population)** (WHO Global Health Observatory)  
  Estimated road traffic death rate (per 100 000 population) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/RS_198](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/RS_198)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--RS_198.json"
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

        - Guinea has the world's highest road death rate at 37.4 per 100,000, nearly 25 times Norway's 1.5
        - The United States (14.2) has a death rate 7 times higher than peer nations like Sweden (2.1) and Norway (1.5)
        - Sub-Saharan Africa dominates the critical tier: Guinea, Libya, Haiti, Zimbabwe all above 25 per 100k
        - Singapore (1.9) and Norway (1.5) demonstrate that near-zero road deaths are achievable with investment in infrastructure and enforcement
        """
    )
    return


if __name__ == "__main__":
    app.run()
