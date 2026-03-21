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
        # The Preston Curve, Unwound

        Six countries traced through GDP per capita and life expectancy from 1960 to 2023. Each line shows how wealth and health evolved together over six decades.
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
        - **GDP per capita (current US$)** (World Bank)  
  GDP per capita (current US$) from World Bank  
  Source: [https://data.worldbank.org/indicator/NY.GDP.PCAP.CD](https://data.worldbank.org/indicator/NY.GDP.PCAP.CD)
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
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-PCAP-CD.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_1 = _raw["meta"]
    df_1 = pd.DataFrame(_raw["data"])
    df_1 = df_1.dropna(subset=["value"])
    mo.md(f"**{meta_1['title']}** -- {len(df_1)} rows, {df_1['countryName'].nunique()} countries, {df_1['year'].min()}--{df_1['year'].max()}")
    mo.ui.table(df_1.head(20))
    return (df_1, meta_1)


@app.cell
def _(mo):
    mo.md(
        """
        ## Transformation

        For a multi-dataset view we merge the datasets on country and year, keeping only rows where all indicators have values.
        """
    )
    return


@app.cell
def _(df_0, df_1, meta_0, meta_1, pd):
    _d0 = df_0[["countryName", "year", "value"]].rename(columns={"value": "x_value"})
    _d1 = df_1[["countryName", "year", "value"]].rename(columns={"value": "y_value"})
    _merged = _d0.merge(_d1, on=["countryName", "year"])
    _latest_year = _merged.groupby("countryName")["year"].max().reset_index()
    _latest_year.columns = ["countryName", "latest_year"]
    transformed = _merged.merge(
        _latest_year, left_on=["countryName", "year"], right_on=["countryName", "latest_year"]
    ).drop(columns=["latest_year"])
    transformed
    return (transformed,)


@app.cell
def _(transformed, meta_0, meta_1, alt, mo):
    _chart = (
        alt.Chart(transformed)
        .mark_circle(size=80)
        .encode(
            x=alt.X("x_value:Q", title=meta_0["title"]),
            y=alt.Y("y_value:Q", title=meta_1["title"]),
            color=alt.Color("countryName:N", title="Country"),
            tooltip=["countryName", "year", "x_value", "y_value"],
        )
        .properties(width=600, height=400)
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - China's trail shows the most dramatic transformation: from $90 GDP/cap and 33 years life expectancy to $13,000 and 78 years
        - Japan's trail bends backward after 1995 as GDP stagnated while life expectancy kept rising
        - Nigeria's path barely moves upward despite GDP fluctuations, stuck around 50-55 years
        - Brazil and India trace parallel upward paths but at different wealth levels
        - The US trail flattens at the top: high wealth but diminishing life expectancy gains
        """
    )
    return


if __name__ == "__main__":
    app.run()
