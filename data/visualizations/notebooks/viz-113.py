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
        # Youth Unemployment Rates Around the World, 2024

        A horizontal bar chart comparing youth unemployment rates (% of labor force ages 15-24) across 28 countries for 2024, spanning the full range from lowest to highest.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Youth Unemployment Rate (% of labor force ages 15-24)** (World Bank / ILO)
  Unemployment, youth total (% of total labor force ages 15-24) (modeled ILO estimate)
  Source: [https://data.worldbank.org/indicator/SL.UEM.1524.ZS](https://data.worldbank.org/indicator/SL.UEM.1524.ZS)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-UEM-1524-ZS.json"
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

        Filter to 2024, exclude aggregate/region codes, select 28 countries evenly spread across the value range, and assign World Bank regions for color coding.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _aggregates = {
        "ZH", "ZI", "1A", "S3", "B8", "V2", "Z4", "4E", "T4", "XC",
        "Z7", "7E", "T7", "EU", "F1", "XE", "XD", "XF", "ZT", "XH",
        "XI", "XG", "V3", "ZJ", "XJ", "T2", "XL", "XO", "XM", "XN",
        "ZQ", "XQ", "XP", "OE", "S4", "S2", "V4", "V1", "S1", "8S",
        "ZG", "ZF", "XT", "1W", "T6", "T5", "JG", "T3",
    }
    _recent = df_0[
        (df_0["year"] == 2024)
        & (~df_0["country"].isin(_aggregates))
        & (df_0["country"].str.len() == 2)
        & (~df_0["country"].str.match(r"^[0-9]"))
    ].copy()
    _recent = _recent.sort_values("value").reset_index(drop=True)

    _n = 28
    _step = (len(_recent) - 1) / (_n - 1)
    _indices = [round(i * _step) for i in range(_n)]
    selected = _recent.iloc[_indices].copy()

    _region_map = {
        "KH": "East Asia & Pacific", "GW": "Sub-Saharan Africa",
        "CI": "Sub-Saharan Africa", "BO": "Latin America & Caribbean",
        "BH": "Middle East & North Africa", "BF": "Sub-Saharan Africa",
        "SV": "Latin America & Caribbean", "HN": "Latin America & Caribbean",
        "KM": "Sub-Saharan Africa", "AU": "East Asia & Pacific",
        "ER": "Sub-Saharan Africa", "IE": "Europe & Central Asia",
        "BG": "Europe & Central Asia", "GU": "East Asia & Pacific",
        "AZ": "Europe & Central Asia", "FJ": "East Asia & Pacific",
        "IN": "South Asia", "EG": "Middle East & North Africa",
        "BT": "South Asia", "FR": "Europe & Central Asia",
        "EE": "Europe & Central Asia", "CR": "Latin America & Caribbean",
        "GY": "Latin America & Caribbean", "AO": "Sub-Saharan Africa",
        "GE": "Europe & Central Asia", "GA": "Sub-Saharan Africa",
        "CG": "Sub-Saharan Africa", "DJ": "Middle East & North Africa",
    }
    selected["region"] = selected["country"].map(_region_map)
    selected["value_rounded"] = selected["value"].round(1)
    selected
    return (selected,)


@app.cell
def _(selected, alt, mo):
    _chart = (
        alt.Chart(selected)
        .mark_bar()
        .encode(
            x=alt.X("value_rounded:Q", title="Youth unemployment rate (%)"),
            y=alt.Y("countryName:N", title=None, sort=alt.EncodingSortField(field="value_rounded", order="ascending")),
            color=alt.Color(
                "region:N",
                title="Region",
                scale=alt.Scale(
                    domain=[
                        "East Asia & Pacific",
                        "Europe & Central Asia",
                        "Latin America & Caribbean",
                        "Middle East & North Africa",
                        "South Asia",
                        "Sub-Saharan Africa",
                    ],
                    range=["#3b82f6", "#8b5cf6", "#f59e0b", "#ef4444", "#10b981", "#f97316"],
                ),
            ),
            tooltip=["countryName:N", "value_rounded:Q", "region:N"],
        )
        .properties(width=550, height=580, title="Youth Unemployment Rates Around the World, 2024")
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Cambodia has the lowest youth unemployment at 0.7%, reflecting high informal labor force participation among young people
        - Djibouti is a dramatic outlier at 76.5%, more than triple the next-highest country (Congo, Rep. at 40.6%)
        - Several Sub-Saharan African countries appear at both extremes, showing wide intra-regional variation
        - European countries cluster in the mid-range (10-20%), with Georgia a notable outlier at 29.9%
        """
    )
    return


if __name__ == "__main__":
    app.run()
