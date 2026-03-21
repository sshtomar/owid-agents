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
        # The Price of a Longer Life

        Health expenditure per capita vs. life expectancy at birth across 85 countries in 2021.
        The scatter plot reveals that initial health spending produces steep gains in longevity,
        but returns flatten sharply beyond ~$1,000 per person.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Health Expenditure per Capita (current US$)** (world-bank)
          Indicator: SH.XPD.CHEX.PC.CD
          Source: [https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD](https://data.worldbank.org/indicator/SH.XPD.CHEX.PC.CD)

        - **Life Expectancy at Birth** (world-bank)
          Indicator: SP.DYN.LE00.IN
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
    import numpy as np
    return json, urllib, pd, alt, np


@app.cell
def _(json, urllib, pd, mo):
    _path_he = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-XPD-CHEX-PC-CD.json"
    try:
        _text = _path_he.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path_he)).read().decode()
    _raw = json.loads(_text)
    meta_he = _raw["meta"]
    df_he = pd.DataFrame(_raw["data"])
    df_he = df_he.dropna(subset=["value"])
    df_he = df_he.rename(columns={"value": "health_exp"})
    mo.md(f"**{meta_he['title']}** -- {len(df_he)} rows, {df_he['countryName'].nunique()} countries, {df_he['year'].min()}--{df_he['year'].max()}")
    return (df_he, meta_he)


@app.cell
def _(json, urllib, pd, mo):
    _path_le = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SP-DYN-LE00-IN.json"
    try:
        _text = _path_le.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path_le)).read().decode()
    _raw = json.loads(_text)
    meta_le = _raw["meta"]
    df_le = pd.DataFrame(_raw["data"])
    df_le = df_le.dropna(subset=["value"])
    df_le = df_le.rename(columns={"value": "life_exp"})
    mo.md(f"**{meta_le['title']}** -- {len(df_le)} rows, {df_le['countryName'].nunique()} countries, {df_le['year'].min()}--{df_le['year'].max()}")
    return (df_le, meta_le)


@app.cell
def _(mo):
    mo.md(
        """
        ## Transformation

        Merge the two datasets on country and year, filter to 2021, and exclude
        World Bank aggregate regions. Assign broad geographic regions for color coding.
        """
    )
    return


@app.cell
def _(df_he, df_le, pd):
    _year = 2021
    _he_yr = df_he[df_he["year"] == _year][["country", "countryName", "health_exp"]].copy()
    _le_yr = df_le[df_le["year"] == _year][["country", "life_exp"]].copy()
    merged = _he_yr.merge(_le_yr, on="country", how="inner")

    _aggregates = {
        "ZH", "ZI", "S3", "V2", "Z4", "4E", "T4", "XC", "Z7", "7E", "T7",
        "EU", "F1", "XE", "XD", "XF", "ZT", "XH", "XI", "XG", "V3", "ZJ",
        "XJ", "T2", "XL", "XO", "XM", "XN", "ZQ", "XQ", "T3", "XP", "XU",
        "OE", "V4", "V1", "S4", "S2", "S1", "8S", "ZG", "ZF", "XT", "1W",
        "1A", "B8", "T5", "T6",
    }
    merged = merged[~merged["country"].isin(_aggregates)].copy()

    _region_map = {
        "AO": "Sub-Saharan Africa", "BJ": "Sub-Saharan Africa", "BW": "Sub-Saharan Africa",
        "BF": "Sub-Saharan Africa", "BI": "Sub-Saharan Africa", "CM": "Sub-Saharan Africa",
        "CV": "Sub-Saharan Africa", "CF": "Sub-Saharan Africa", "TD": "Sub-Saharan Africa",
        "KM": "Sub-Saharan Africa", "CG": "Sub-Saharan Africa", "CD": "Sub-Saharan Africa",
        "CI": "Sub-Saharan Africa", "DJ": "Sub-Saharan Africa", "GQ": "Sub-Saharan Africa",
        "ER": "Sub-Saharan Africa", "SZ": "Sub-Saharan Africa", "ET": "Sub-Saharan Africa",
        "GA": "Sub-Saharan Africa", "GM": "Sub-Saharan Africa", "GH": "Sub-Saharan Africa",
        "GN": "Sub-Saharan Africa", "GW": "Sub-Saharan Africa", "KE": "Sub-Saharan Africa",
        "LS": "Sub-Saharan Africa", "LR": "Sub-Saharan Africa", "MG": "Sub-Saharan Africa",
        "MW": "Sub-Saharan Africa", "ML": "Sub-Saharan Africa", "MR": "Sub-Saharan Africa",
        "MU": "Sub-Saharan Africa", "MZ": "Sub-Saharan Africa", "NA": "Sub-Saharan Africa",
        "NE": "Sub-Saharan Africa", "NG": "Sub-Saharan Africa", "RW": "Sub-Saharan Africa",
        "ST": "Sub-Saharan Africa", "SN": "Sub-Saharan Africa", "SC": "Sub-Saharan Africa",
        "SL": "Sub-Saharan Africa", "SO": "Sub-Saharan Africa", "ZA": "Sub-Saharan Africa",
        "SS": "Sub-Saharan Africa", "SD": "Sub-Saharan Africa", "TZ": "Sub-Saharan Africa",
        "TG": "Sub-Saharan Africa", "UG": "Sub-Saharan Africa", "ZM": "Sub-Saharan Africa",
        "ZW": "Sub-Saharan Africa",
        "AL": "Europe", "AT": "Europe", "AZ": "Europe", "BY": "Europe", "BE": "Europe",
        "BA": "Europe", "BG": "Europe", "HR": "Europe", "CY": "Europe", "CZ": "Europe",
        "DK": "Europe", "EE": "Europe", "FI": "Europe", "FR": "Europe", "GE": "Europe",
        "DE": "Europe", "GR": "Europe", "HU": "Europe", "IS": "Europe", "IE": "Europe",
        "IT": "Europe", "KZ": "Europe", "KG": "Europe", "LV": "Europe", "LT": "Europe",
        "LU": "Europe", "MK": "Europe", "MT": "Europe", "MD": "Europe", "ME": "Europe",
        "NL": "Europe", "NO": "Europe", "PL": "Europe", "PT": "Europe", "RO": "Europe",
        "RU": "Europe", "RS": "Europe", "SK": "Europe", "SI": "Europe", "ES": "Europe",
        "SE": "Europe", "CH": "Europe", "TJ": "Europe", "TR": "Europe", "TM": "Europe",
        "UA": "Europe", "GB": "Europe", "UZ": "Europe", "XK": "Europe", "AM": "Europe",
        "AD": "Europe",
        "AU": "East Asia & Pacific", "BN": "East Asia & Pacific", "KH": "East Asia & Pacific",
        "CN": "East Asia & Pacific", "FJ": "East Asia & Pacific", "ID": "East Asia & Pacific",
        "JP": "East Asia & Pacific", "KR": "East Asia & Pacific", "LA": "East Asia & Pacific",
        "MY": "East Asia & Pacific", "MN": "East Asia & Pacific", "MM": "East Asia & Pacific",
        "NZ": "East Asia & Pacific", "PH": "East Asia & Pacific", "SG": "East Asia & Pacific",
        "TH": "East Asia & Pacific", "VN": "East Asia & Pacific",
        "AF": "South Asia", "BD": "South Asia", "BT": "South Asia", "IN": "South Asia",
        "MV": "South Asia", "NP": "South Asia", "PK": "South Asia", "LK": "South Asia",
        "DZ": "Middle East & N. Africa", "BH": "Middle East & N. Africa",
        "EG": "Middle East & N. Africa", "IR": "Middle East & N. Africa",
        "IQ": "Middle East & N. Africa", "IL": "Middle East & N. Africa",
        "JO": "Middle East & N. Africa", "KW": "Middle East & N. Africa",
        "LB": "Middle East & N. Africa", "MA": "Middle East & N. Africa",
        "QA": "Middle East & N. Africa", "SA": "Middle East & N. Africa",
        "TN": "Middle East & N. Africa", "AE": "Middle East & N. Africa",
        "YE": "Middle East & N. Africa",
        "AR": "Latin America", "BO": "Latin America", "BR": "Latin America",
        "CL": "Latin America", "CO": "Latin America", "CR": "Latin America",
        "CU": "Latin America", "DO": "Latin America", "EC": "Latin America",
        "SV": "Latin America", "GT": "Latin America", "HT": "Latin America",
        "HN": "Latin America", "JM": "Latin America", "MX": "Latin America",
        "NI": "Latin America", "PA": "Latin America", "PY": "Latin America",
        "PE": "Latin America", "UY": "Latin America", "VE": "Latin America",
        "BS": "Latin America", "BB": "Latin America", "BZ": "Latin America",
        "GY": "Latin America", "SR": "Latin America", "TT": "Latin America",
        "CA": "North America", "US": "North America",
    }
    merged["region"] = merged["country"].map(_region_map)
    merged = merged.dropna(subset=["region"])
    merged = merged.sort_values("health_exp")
    merged
    return (merged,)


@app.cell
def _(merged, alt, mo):
    _region_order = [
        "Sub-Saharan Africa", "South Asia", "Middle East & N. Africa",
        "Latin America", "East Asia & Pacific", "Europe", "North America",
    ]
    _color_range = ["#e15759", "#b07aa1", "#edc948", "#59a14f", "#f28e2b", "#4e79a7", "#76b7b2"]

    _scatter = (
        alt.Chart(merged)
        .mark_circle(size=80, opacity=0.7)
        .encode(
            x=alt.X(
                "health_exp:Q",
                title="Health expenditure per capita (US$, log scale)",
                scale=alt.Scale(type="log", domain=[15, 10000]),
            ),
            y=alt.Y(
                "life_exp:Q",
                title="Life expectancy at birth (years)",
                scale=alt.Scale(domain=[38, 86]),
            ),
            color=alt.Color(
                "region:N",
                title="Region",
                scale=alt.Scale(domain=_region_order, range=_color_range),
            ),
            tooltip=[
                alt.Tooltip("countryName:N", title="Country"),
                alt.Tooltip("health_exp:Q", title="Health Spending ($)", format=",.0f"),
                alt.Tooltip("life_exp:Q", title="Life Expectancy (yrs)", format=".1f"),
                alt.Tooltip("region:N", title="Region"),
            ],
        )
        .properties(width=700, height=450, title="The Price of a Longer Life (2021)")
    )
    mo.ui.altair_chart(_scatter)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Japan leads with 84.5 years of life expectancy on $4,844 per capita health spending, outperforming countries that spend 50% more
        - Bangladesh achieves 71 years of life expectancy on just $56 per capita, the most efficient health outcome among South Asian nations
        - Central African Republic is the starkest outlier at 40.3 years and $46 per capita, nearly 20 years below its spending peers
        - Botswana and Eswatini spend $300-500 per capita but achieve lower life expectancy than countries spending $30, likely reflecting the HIV/AIDS burden
        """
    )
    return


if __name__ == "__main__":
    app.run()
