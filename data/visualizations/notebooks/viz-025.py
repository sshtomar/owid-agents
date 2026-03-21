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
        # The Price of Prices

        Inflation rate (annual % change in consumer prices) for 10 countries from 2000 to 2030. Uses a symlog scale to handle Venezuela's 65,374% hyperinflation alongside Japan's deflation. IMF projections shown as dashed lines.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Inflation Rate (annual % change)** (imf)  
  Inflation Rate (annual % change) from imf  
  Source: [https://www.imf.org/external/datamapper/PCPIPCH](https://www.imf.org/external/datamapper/PCPIPCH)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "imf--PCPIPCH.json"
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

        - Venezuela's inflation peaked at 65,374% in 2018 before collapsing under dollarization
        - Argentina surged to 220% in 2024 before IMF projects a dramatic decline under Milei's reforms
        - Turkey tamed inflation to single digits by 2004 only to see it resurge past 72% in 2022
        - Japan spent over two decades in deflation, only recently seeing positive inflation
        """
    )
    return


if __name__ == "__main__":
    app.run()
