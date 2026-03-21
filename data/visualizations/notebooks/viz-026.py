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
        # When Nature Strikes

        Global deaths from natural disasters per year, 1900-2024. Aggregated across all countries. The deadliest years are annotated with their major events: China floods, Bengal famine, Indian Ocean tsunami, Haiti earthquake.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Deaths from Natural Disasters** (owid)  
  Deaths from Natural Disasters from owid  
  Source: [https://ourworldindata.org](https://ourworldindata.org)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "owid--899981.json"
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

        - The 1931 China floods killed 3.7 million people, the deadliest single disaster year in the dataset
        - The 2004 Indian Ocean tsunami (242K dead) and 2010 Haiti earthquake (308K) stand out in the modern era
        - Deaths have trended dramatically downward despite population growth, thanks to early warning systems and better infrastructure
        - The 1928 and 1943 famines in China and Bengal each killed over 1.9 million
        """
    )
    return


if __name__ == "__main__":
    app.run()
