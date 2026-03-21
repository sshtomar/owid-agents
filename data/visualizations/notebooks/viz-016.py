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
        # The Vaccine Shield

        DTP3 immunization coverage among 1-year-olds (%) for 12 countries from 2000 to 2024. Conflict, instability, and health system strength produce starkly different trajectories.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Diphtheria tetanus toxoid and pertussis (DTP3) immunization coverage among 1-year-olds (%)** (WHO Global Health Observatory)  
  Diphtheria tetanus toxoid and pertussis (DTP3) immunization coverage among 1-year-olds (%) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/WHS4_100](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/WHS4_100)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHS4_100.json"
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

        - North Korea climbed from 56% in 2000 to 99% by 2021
        - Brazil and Romania both fell from near-universal coverage (98-99%) to below 80%
        - India rose steadily from 59% to 91%, crossing the WHO 90% target threshold by 2023
        - Yemen and Papua New Guinea remain far below the 90% target with no sign of recovery
        """
    )
    return


if __name__ == "__main__":
    app.run()
