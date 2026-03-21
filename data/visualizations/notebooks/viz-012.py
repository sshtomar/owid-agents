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
        # The Malaria Frontier

        Estimated malaria incidence per 1,000 population at risk across 16 high-burden countries from 2000 to 2024. Most of Sub-Saharan Africa has seen real but uneven progress.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Estimated malaria incidence (per 1000 population at risk)** (WHO Global Health Observatory)  
  Estimated malaria incidence (per 1000 population at risk) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/MALARIA_EST_INCIDENCE](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/MALARIA_EST_INCIDENCE)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--MALARIA_EST_INCIDENCE.json"
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

        - Senegal achieved the steepest decline, falling from 177 to 35 per 1,000 -- an 80% reduction
        - Ethiopia cut its incidence by 76%, from 189 to 46 per 1,000
        - Tanzania and Ghana each dropped by more than 55%
        - Niger and Mali made the least progress, remaining above 300-340 per 1,000 through 2023
        """
    )
    return


if __name__ == "__main__":
    app.run()
