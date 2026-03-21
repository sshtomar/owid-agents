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
        # Red Ink

        Government fiscal balance (net lending/borrowing) as % of GDP for 23 countries, 2025 IMF estimates. Diverging bar chart from Kuwait's +26.8% surplus to China's -8.6% deficit. Oil exporters dominate the surplus side.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Government Net Lending/Borrowing (% of GDP)** (imf)  
  Government Net Lending/Borrowing (% of GDP) from imf  
  Source: [https://www.imf.org/external/datamapper/GGXCNL_NGDP](https://www.imf.org/external/datamapper/GGXCNL_NGDP)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "imf--GGXCNL_NGDP.json"
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

        - Kuwait runs the largest fiscal surplus at 26.8% of GDP, driven entirely by oil revenues
        - China (-8.6%) and Brazil (-8.4%) run the largest deficits among major economies
        - The United States deficit of -7.4% places it among the world's biggest borrowers
        - Norway (+12.7%) channels oil wealth into its sovereign wealth fund, maintaining strong surpluses
        """
    )
    return


if __name__ == "__main__":
    app.run()
