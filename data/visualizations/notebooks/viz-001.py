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
        # The Great Convergence

        Life expectancy at birth in 1960 vs 2023 for 21 countries. Sixty years ago, a child born in Japan could expect 34 more years of life than one born in Afghanistan. Today that gap has narrowed to 18 years.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Life expectancy at birth, total (years)** (World Bank)  
  Life expectancy at birth, total (years) from World Bank  
  Source: [https://data.worldbank.org/indicator/SP.DYN.LE00.IN](https://data.worldbank.org/indicator/SP.DYN.LE00.IN)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-LE00-IN.json"
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

        For a before/after view we take the earliest and latest observation per country and compute the change over time.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _earliest = df_0.loc[df_0.groupby("countryName")["year"].idxmin()][["countryName", "year", "value"]]
    _earliest.columns = ["countryName", "start_year", "start_value"]
    _latest = df_0.loc[df_0.groupby("countryName")["year"].idxmax()][["countryName", "year", "value"]]
    _latest.columns = ["countryName", "end_year", "end_value"]
    _merged = _earliest.merge(_latest, on="countryName")
    _merged["delta"] = _merged["end_value"] - _merged["start_value"]
    transformed = _merged.sort_values("delta", ascending=False).head(20).copy()
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, pd, mo):
    _start = transformed[["countryName", "start_year", "start_value"]].rename(
        columns={"start_year": "year", "start_value": "value"}
    )
    _start["period"] = "start"
    _end = transformed[["countryName", "end_year", "end_value"]].rename(
        columns={"end_year": "year", "end_value": "value"}
    )
    _end["period"] = "end"
    _plot_df = pd.concat([_start, _end], ignore_index=True)

    _lines = (
        alt.Chart(_plot_df)
        .mark_line()
        .encode(
            x=alt.X("period:N", title="Period", sort=["start", "end"]),
            y=alt.Y("value:Q", title="Value"),
            detail="countryName:N",
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "period", "value"],
        )
    )
    _points = (
        alt.Chart(_plot_df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("period:N", sort=["start", "end"]),
            y=alt.Y("value:Q"),
            color=alt.Color("countryName:N"),
            tooltip=["countryName", "period", "year", "value"],
        )
    )
    _chart = (_lines + _points).properties(width=500, height=400)
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - China gained 44.5 years of life expectancy, the largest absolute gain of any country shown
        - Iran, Afghanistan, and Bangladesh each gained more than 30 years
        - Rich nations in 1960 gained 11-16 years; poor nations gained 15-44 years, showing convergence
        - Chad and Central African Republic remain below 58 years despite gains
        """
    )
    return


if __name__ == "__main__":
    app.run()
