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
        # The Silent Epidemic

        Suicide mortality rates (per 100,000 population) across 31 countries, ranging from Guyana's 76.9 to Kuwait's 0.7. Color-coded by severity: red for rates above 25, amber for 10-25, green below 10.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Crude suicide rates (per 100 000 population)** (WHO Global Health Observatory)  
  Crude suicide rates (per 100 000 population) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/SDGSUICIDE](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/SDGSUICIDE)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--SDGSUICIDE.json"
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

        - Guyana leads at 76.9 per 100,000, more than 100 times higher than Kuwait's 0.7
        - Former Soviet states cluster in the high-rate tier: Russia (27.1), Ukraine (27.9), Kazakhstan (40.9), Estonia (39.1)
        - China (38.5) and Hungary (35.9) have unexpectedly high rates among middle-income and EU nations
        - Gulf states and Caribbean islands cluster near zero, likely reflecting both cultural factors and underreporting
        """
    )
    return


if __name__ == "__main__":
    app.run()
