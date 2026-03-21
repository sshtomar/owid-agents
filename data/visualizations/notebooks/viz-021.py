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
        # Forced From Home

        Number of refugees by country of origin from 2000 to 2024, highlighting the world's largest displacement crises. UNHCR data traces the rise and fall of refugee populations from Syria, Afghanistan, Ukraine, and other conflict zones.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Refugees by Country of Origin** (unhcr)  
  Refugees by Country of Origin from unhcr  
  Source: [https://www.unhcr.org/refugee-statistics/](https://www.unhcr.org/refugee-statistics/)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "unhcr--refugees.json"
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

        - Syria's refugee population exploded from near zero in 2011 to over 6.5 million by 2016, making it the world's largest source of refugees
        - Afghanistan has been a top-3 refugee source for over two decades, with numbers climbing back above 6 million after the 2021 Taliban takeover
        - Ukraine generated the fastest-ever refugee crisis, surging from negligible numbers to over 6 million in a single year (2022)
        - South Sudan and Myanmar each produced over a million refugees following civil conflict and military coups
        """
    )
    return


if __name__ == "__main__":
    app.run()
