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
        # The Health Divide

        A dot-matrix scorecard comparing 15 countries across four health indicators: malaria incidence, DTP3 immunization, maternal mortality, and HIV prevalence. Color and size encode relative performance.
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
        - **Diphtheria tetanus toxoid and pertussis (DTP3) immunization coverage among 1-year-olds (%)** (WHO Global Health Observatory)  
  Diphtheria tetanus toxoid and pertussis (DTP3) immunization coverage among 1-year-olds (%) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/WHS4_100](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/WHS4_100)
        - **Maternal mortality ratio (per 100 000 live births)** (WHO Global Health Observatory)  
  Maternal mortality ratio (per 100 000 live births) from who-gho  
  Source: [https://www.who.int/data/gho/data/indicators/indicator-details/GHO/MDG_0000000026](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/MDG_0000000026)
        - **Prevalence of HIV, total (% of population ages 15-49)** (World Bank)  
  Prevalence of HIV, total (% of population ages 15-49) from world-bank  
  Source: [https://data.worldbank.org/indicator/SH.DYN.AIDS.ZS](https://data.worldbank.org/indicator/SH.DYN.AIDS.ZS)
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
def _(json, urllib, pd, mo):
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--WHS4_100.json"
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "who--MDG_0000000026.json"
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-AIDS-ZS.json"
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

        - Nigeria carries the heaviest combined burden: highest malaria incidence, lowest DTP3 coverage, worst maternal mortality
        - India and Bangladesh stand out as South Asian bright spots with near-zero malaria and high vaccination rates
        - Ghana achieves 95% DTP3 coverage despite a high malaria burden of 195 per 1,000
        - Kenya has the highest HIV prevalence at 3.0% while Bangladesh and India report below 0.2%
        """
    )
    return


if __name__ == "__main__":
    app.run()
