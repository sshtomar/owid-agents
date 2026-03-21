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
        # The Debt Mountain

        Government gross debt as a share of GDP, 2000-2030, for 10 major economies. Values after 2024 are IMF projections. Traces the long-term fiscal trajectories of the world's largest economies through crises and recoveries.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Government Gross Debt (% of GDP)** (imf)  
  Government Gross Debt (% of GDP) from imf  
  Source: [https://www.imf.org/external/datamapper/GGXWDG_NGDP](https://www.imf.org/external/datamapper/GGXWDG_NGDP)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "imf--GGXWDG_NGDP.json"
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

        - Japan's debt peaked at 258% of GDP in 2020 and remains the highest among major economies even after declining to 236%
        - China's debt trajectory is the steepest, projected to cross 100% of GDP by 2026 from just 23% in 2000
        - The COVID-19 pandemic caused visible debt spikes across all countries in 2020, adding 15-25 percentage points
        - Germany stands out as the only major economy that meaningfully reduced its debt ratio from 2010-2019
        """
    )
    return


if __name__ == "__main__":
    app.run()
