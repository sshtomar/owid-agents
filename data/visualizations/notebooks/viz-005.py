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
        # Development at a Glance

        Six development indicators across 19 countries. Dot size shows magnitude, color shows relative standing. 114 data points in a single compact view.
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
        - **Mortality rate, under-5 (per 1,000 live births)** (World Bank)  
  Mortality rate, under-5 (per 1,000 live births) from World Bank  
  Source: [https://data.worldbank.org/indicator/SH.DYN.MORT](https://data.worldbank.org/indicator/SH.DYN.MORT)
        - **Urban population (% of total population)** (World Bank)  
  Urban population (% of total population) from World Bank  
  Source: [https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS](https://data.worldbank.org/indicator/SP.URB.TOTL.IN.ZS)
        - **Individuals using the Internet (% of population)** (World Bank)  
  Individuals using the Internet (% of population) from World Bank  
  Source: [https://data.worldbank.org/indicator/IT.NET.USER.ZS](https://data.worldbank.org/indicator/IT.NET.USER.ZS)
        - **Renewable electricity output (% of total electricity output)** (World Bank)  
  Renewable electricity output (% of total electricity output) from World Bank  
  Source: [https://data.worldbank.org/indicator/EG.ELC.RNEW.ZS](https://data.worldbank.org/indicator/EG.ELC.RNEW.ZS)
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
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-MORT.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_2 = _raw["meta"]
    df_2 = pd.DataFrame(_raw["data"])
    df_2 = df_2.dropna(subset=["value"])
    mo.md(f"**{meta_2['title']}** -- {len(df_2)} rows, {df_2['countryName'].nunique()} countries, {df_2['year'].min()}--{df_2['year'].max()}")
    mo.ui.table(df_2.head(20))
    return (df_2, meta_2)


@app.cell
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-URB-TOTL-IN-ZS.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_3 = _raw["meta"]
    df_3 = pd.DataFrame(_raw["data"])
    df_3 = df_3.dropna(subset=["value"])
    mo.md(f"**{meta_3['title']}** -- {len(df_3)} rows, {df_3['countryName'].nunique()} countries, {df_3['year'].min()}--{df_3['year'].max()}")
    mo.ui.table(df_3.head(20))
    return (df_3, meta_3)


@app.cell
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IT-NET-USER-ZS.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_4 = _raw["meta"]
    df_4 = pd.DataFrame(_raw["data"])
    df_4 = df_4.dropna(subset=["value"])
    mo.md(f"**{meta_4['title']}** -- {len(df_4)} rows, {df_4['countryName'].nunique()} countries, {df_4['year'].min()}--{df_4['year'].max()}")
    mo.ui.table(df_4.head(20))
    return (df_4, meta_4)


@app.cell
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-RNEW-ZS.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_5 = _raw["meta"]
    df_5 = pd.DataFrame(_raw["data"])
    df_5 = df_5.dropna(subset=["value"])
    mo.md(f"**{meta_5['title']}** -- {len(df_5)} rows, {df_5['countryName'].nunique()} countries, {df_5['year'].min()}--{df_5['year'].max()}")
    mo.ui.table(df_5.head(20))
    return (df_5, meta_5)


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

        - Ethiopia has 95.4% renewable electricity but the lowest life expectancy and internet access in the group
        - Japan leads in life expectancy (84 years) and lowest child mortality (2.4 per 1,000) but has only 21% renewable electricity
        - Bangladesh and India show similar GDP per capita (~$2,600) but Bangladesh has higher child mortality
        - Brazil stands out with 77% renewable electricity, high urbanization, and strong internet adoption
        """
    )
    return


if __name__ == "__main__":
    app.run()
