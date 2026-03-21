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
        # Democracy's Ebb and Flow

        Electoral Democracy Index (0-1 scale) for 12 countries from 1970 to 2025, grouped by regime trajectory: stable democracies (Sweden, USA), democratization stories (Chile, South Korea, South Africa), democratic backsliders (Hungary, Poland, Turkey, India), and persistent autocracies (Russia, China, Saudi Arabia).
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Electoral Democracy Index (0-1)** (owid)  
  Electoral Democracy Index (0-1) from owid  
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "owid--1209753.json"
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

        - Hungary and Poland surged past 0.85 after 1990 but have slid sharply since 2010-2016 under Orban and PiS; Poland recovered noticeably after 2023
        - Turkey peaked near 0.66 in 2004 during EU-accession reforms, then fell below 0.3 by 2017 following Erdogan's consolidation of power
        - Chile and South Korea both transitioned from sub-0.15 autocracy to above-0.8 democracy within a single decade (1987-1993)
        - Saudi Arabia has remained flat near 0.015 for 55 years -- the least democratic score in the dataset throughout the entire period
        """
    )
    return


if __name__ == "__main__":
    app.run()
