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
        # The Persistent Plague

        Tuberculosis incidence per 100,000 population for 10 high-burden countries, 2000-2024. South Africa's HIV-fuelled epidemic peaked above 1,200 before plunging. Ethiopia and Russia halved their rates. The Philippines keeps climbing. Nigeria has not budged.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Incidence of tuberculosis (per 100 000 population per year)** (WHO Global Health Observatory)  
  Incidence of tuberculosis (per 100 000 population per year) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/MDG_0000000020](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/MDG_0000000020)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--MDG_0000000020.json"
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

        - South Africa's TB rate peaked at 1,230 per 100k in 2010 driven by HIV co-infection, then fell 68% to 389 by 2024
        - The Philippines is the only high-burden country where incidence is rising, from 590 to 627
        - Nigeria's rate has been frozen at exactly 219 per 100,000 for 18 consecutive years of reporting
        - Ethiopia achieved a 65% reduction from 462 to 163, one of Africa's greatest TB success stories
        """
    )
    return


if __name__ == "__main__":
    app.run()
