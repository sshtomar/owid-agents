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
        # Out of the Smoke

        Access to clean fuels and technologies for cooking (% of population) from 2000 to 2023 for 12 countries. India's transformation from 23% to 77% stands out. Indonesia leapt from 7% to 91%. Ethiopia barely reached 7%.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Access to clean fuels and technologies for cooking (% of population)** (World Bank)  
  Access to clean fuels and technologies for cooking (% of population) from world-bank  
  Source: [https://data.worldbank.org/indicator/EG.CFT.ACCS.ZS](https://data.worldbank.org/indicator/EG.CFT.ACCS.ZS)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-CFT-ACCS-ZS.json"
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

        - Indonesia achieved the most dramatic transformation: from 6.7% to 90.6% clean fuel access in 23 years
        - India's Ujjwala Yojana program drove access from 22.7% to 76.7%, lifting hundreds of millions out of solid fuel dependence
        - China went from 40.3% to 88.7%, driven by urbanization and natural gas infrastructure
        - Ethiopia remains at just 7.1% -- nearly the entire population still cooks with wood, charcoal, or dung
        """
    )
    return


if __name__ == "__main__":
    app.run()
