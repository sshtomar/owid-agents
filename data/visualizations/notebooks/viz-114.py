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
        # The U-Shape of Female Labor: Work, Wealth, and Gender

        Scatter plot of female labor force participation vs GDP per capita (log scale) for 85 countries in 2023. Reveals the well-documented U-shaped pattern: women in low-income agrarian economies participate at high rates, participation drops sharply in middle-income countries (especially in the Middle East and South Asia), then rises again in wealthy nations.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Female Labor Force Participation (% of female population 15+)** (World Bank)
          Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)
          Source: [https://data.worldbank.org/indicator/SL.TLF.CACT.FE.ZS](https://data.worldbank.org/indicator/SL.TLF.CACT.FE.ZS)

        - **GDP per Capita (current US$)** (World Bank)
          GDP per capita (current US$)
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
    import numpy as np
    return json, urllib, pd, alt, np


@app.cell
def _(json, urllib, pd, mo):
    _path_lfp = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SL-TLF-CACT-FE-ZS.json"
    try:
        _text = _path_lfp.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path_lfp)).read().decode()
    _raw = json.loads(_text)
    meta_lfp = _raw["meta"]
    df_lfp = pd.DataFrame(_raw["data"])
    df_lfp = df_lfp.dropna(subset=["value"])
    mo.md(f"**{meta_lfp['title']}** -- {len(df_lfp)} rows, {df_lfp['countryName'].nunique()} countries, {df_lfp['year'].min()}--{df_lfp['year'].max()}")
    return (df_lfp, meta_lfp)


@app.cell
def _(json, urllib, pd, mo):
    _path_gdp = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-PCAP-CD.json"
    try:
        _text = _path_gdp.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path_gdp)).read().decode()
    _raw = json.loads(_text)
    meta_gdp = _raw["meta"]
    df_gdp = pd.DataFrame(_raw["data"])
    df_gdp = df_gdp.dropna(subset=["value"])
    mo.md(f"**{meta_gdp['title']}** -- {len(df_gdp)} rows, {df_gdp['countryName'].nunique()} countries, {df_gdp['year'].min()}--{df_gdp['year'].max()}")
    return (df_gdp, meta_gdp)


@app.cell
def _(mo):
    mo.md(
        """
        ## Transformation

        We merge both indicators for 2023, exclude aggregate/regional codes, assign World Bank regions, and identify notable outlier countries for labeling.
        """
    )
    return


@app.cell
def _(df_lfp, df_gdp, pd):
    _aggregates = {
        "ZH","ZI","1A","S3","B8","V2","Z4","4E","T4","XC","Z7","7E","T7","EU","F1",
        "XE","XD","XF","ZT","XH","XI","XG","V3","ZJ","XJ","T2","XL","XO","XM","XN",
        "ZQ","XQ","T3","XP","XU","OE","S4","S2","V4","V1","S1","8S","T5","ZG","ZF",
        "T6","XT","1W","JG"
    }
    _region_map = {
        "AO":"Sub-Saharan Africa","BJ":"Sub-Saharan Africa","BW":"Sub-Saharan Africa","BF":"Sub-Saharan Africa",
        "BI":"Sub-Saharan Africa","CV":"Sub-Saharan Africa","CM":"Sub-Saharan Africa","CF":"Sub-Saharan Africa",
        "TD":"Sub-Saharan Africa","KM":"Sub-Saharan Africa","CD":"Sub-Saharan Africa","CG":"Sub-Saharan Africa",
        "CI":"Sub-Saharan Africa","ER":"Sub-Saharan Africa","SZ":"Sub-Saharan Africa","ET":"Sub-Saharan Africa",
        "GA":"Sub-Saharan Africa","GM":"Sub-Saharan Africa","GH":"Sub-Saharan Africa","GN":"Sub-Saharan Africa",
        "GW":"Sub-Saharan Africa","KE":"Sub-Saharan Africa","LS":"Sub-Saharan Africa","LR":"Sub-Saharan Africa",
        "MG":"Sub-Saharan Africa","MW":"Sub-Saharan Africa","ML":"Sub-Saharan Africa","MR":"Sub-Saharan Africa",
        "MU":"Sub-Saharan Africa","MZ":"Sub-Saharan Africa","NA":"Sub-Saharan Africa","NE":"Sub-Saharan Africa",
        "NG":"Sub-Saharan Africa","RW":"Sub-Saharan Africa","ST":"Sub-Saharan Africa","SN":"Sub-Saharan Africa",
        "SC":"Sub-Saharan Africa","SL":"Sub-Saharan Africa","SO":"Sub-Saharan Africa","ZA":"Sub-Saharan Africa",
        "SS":"Sub-Saharan Africa","SD":"Sub-Saharan Africa","TZ":"Sub-Saharan Africa","TG":"Sub-Saharan Africa",
        "UG":"Sub-Saharan Africa","ZM":"Sub-Saharan Africa","ZW":"Sub-Saharan Africa",
        "AU":"East Asia & Pacific","BN":"East Asia & Pacific","KH":"East Asia & Pacific","CN":"East Asia & Pacific",
        "FJ":"East Asia & Pacific","ID":"East Asia & Pacific","JP":"East Asia & Pacific","KR":"East Asia & Pacific",
        "LA":"East Asia & Pacific","MY":"East Asia & Pacific","MN":"East Asia & Pacific","MM":"East Asia & Pacific",
        "NZ":"East Asia & Pacific","PG":"East Asia & Pacific","PH":"East Asia & Pacific","WS":"East Asia & Pacific",
        "SG":"East Asia & Pacific","SB":"East Asia & Pacific","TH":"East Asia & Pacific","TL":"East Asia & Pacific",
        "TO":"East Asia & Pacific","VU":"East Asia & Pacific","VN":"East Asia & Pacific",
        "AL":"Europe & Central Asia","AM":"Europe & Central Asia","AT":"Europe & Central Asia","AZ":"Europe & Central Asia",
        "BY":"Europe & Central Asia","BE":"Europe & Central Asia","BA":"Europe & Central Asia","BG":"Europe & Central Asia",
        "HR":"Europe & Central Asia","CY":"Europe & Central Asia","CZ":"Europe & Central Asia","DK":"Europe & Central Asia",
        "EE":"Europe & Central Asia","FI":"Europe & Central Asia","FR":"Europe & Central Asia","GE":"Europe & Central Asia",
        "DE":"Europe & Central Asia","GR":"Europe & Central Asia","HU":"Europe & Central Asia","IS":"Europe & Central Asia",
        "IE":"Europe & Central Asia","IT":"Europe & Central Asia","KZ":"Europe & Central Asia","KG":"Europe & Central Asia",
        "LV":"Europe & Central Asia","LT":"Europe & Central Asia","LU":"Europe & Central Asia","MK":"Europe & Central Asia",
        "MD":"Europe & Central Asia","ME":"Europe & Central Asia","NL":"Europe & Central Asia","NO":"Europe & Central Asia",
        "PL":"Europe & Central Asia","PT":"Europe & Central Asia","RO":"Europe & Central Asia","RU":"Europe & Central Asia",
        "RS":"Europe & Central Asia","SK":"Europe & Central Asia","SI":"Europe & Central Asia","ES":"Europe & Central Asia",
        "SE":"Europe & Central Asia","CH":"Europe & Central Asia","TJ":"Europe & Central Asia","TR":"Europe & Central Asia",
        "TM":"Europe & Central Asia","UA":"Europe & Central Asia","GB":"Europe & Central Asia","UZ":"Europe & Central Asia",
        "AR":"Latin America & Caribbean","BS":"Latin America & Caribbean","BB":"Latin America & Caribbean",
        "BZ":"Latin America & Caribbean","BO":"Latin America & Caribbean","BR":"Latin America & Caribbean",
        "CL":"Latin America & Caribbean","CO":"Latin America & Caribbean","CR":"Latin America & Caribbean",
        "CU":"Latin America & Caribbean","DO":"Latin America & Caribbean","EC":"Latin America & Caribbean",
        "SV":"Latin America & Caribbean","GT":"Latin America & Caribbean","GY":"Latin America & Caribbean",
        "HT":"Latin America & Caribbean","HN":"Latin America & Caribbean","JM":"Latin America & Caribbean",
        "MX":"Latin America & Caribbean","NI":"Latin America & Caribbean","PA":"Latin America & Caribbean",
        "PY":"Latin America & Caribbean","PE":"Latin America & Caribbean","SR":"Latin America & Caribbean",
        "TT":"Latin America & Caribbean","UY":"Latin America & Caribbean","VE":"Latin America & Caribbean",
        "DZ":"Middle East & North Africa","BH":"Middle East & North Africa","EG":"Middle East & North Africa",
        "IR":"Middle East & North Africa","IQ":"Middle East & North Africa","IL":"Middle East & North Africa",
        "JO":"Middle East & North Africa","KW":"Middle East & North Africa","LB":"Middle East & North Africa",
        "LY":"Middle East & North Africa","MA":"Middle East & North Africa","OM":"Middle East & North Africa",
        "QA":"Middle East & North Africa","SA":"Middle East & North Africa","TN":"Middle East & North Africa",
        "AE":"Middle East & North Africa","YE":"Middle East & North Africa",
        "CA":"North America","US":"North America",
        "AF":"South Asia","BD":"South Asia","BT":"South Asia","IN":"South Asia",
        "MV":"South Asia","NP":"South Asia","PK":"South Asia","LK":"South Asia",
    }

    _lfp_2023 = df_lfp[df_lfp["year"] == 2023].copy()
    _lfp_2023 = _lfp_2023[~_lfp_2023["country"].isin(_aggregates)]
    _lfp_2023 = _lfp_2023.rename(columns={"value": "lfp"})

    _gdp_2023 = df_gdp[df_gdp["year"] == 2023].copy()
    _gdp_2023 = _gdp_2023[~_gdp_2023["country"].isin(_aggregates)]
    _gdp_2023 = _gdp_2023.rename(columns={"value": "gdp"})

    merged = _lfp_2023[["country", "countryName", "lfp"]].merge(
        _gdp_2023[["country", "gdp"]], on="country"
    )
    merged["region"] = merged["country"].map(_region_map).fillna("Other")
    merged = merged.sort_values("gdp").reset_index(drop=True)
    merged
    return (merged,)


@app.cell
def _(merged, alt, np):
    _notable = {"AF","BI","BJ","KH","IN","IR","IQ","BR","CN","JP","IS","IE","ET"}

    _base = alt.Chart(merged).encode(
        x=alt.X("gdp:Q", scale=alt.Scale(type="log"), title="GDP per capita (current US$, log scale)"),
        y=alt.Y("lfp:Q", title="Female labor force participation (%)"),
        color=alt.Color("region:N", title="Region", scale=alt.Scale(
            domain=["Sub-Saharan Africa","South Asia","Middle East & North Africa",
                     "Latin America & Caribbean","East Asia & Pacific","Europe & Central Asia",
                     "North America","Other"],
            range=["#e07a3a","#9d68c9","#b83f5f","#eeca3b","#4c78a8","#72b7b2","#54a24b","#999999"]
        )),
        tooltip=["countryName:N","gdp:Q","lfp:Q","region:N"]
    )

    _points = _base.mark_circle(size=80, opacity=0.75, stroke="#fff", strokeWidth=0.5)

    _labels = alt.Chart(
        merged[merged["country"].isin(_notable)]
    ).mark_text(dx=10, fontSize=9, fontWeight=500, color="#334155").encode(
        x=alt.X("gdp:Q", scale=alt.Scale(type="log")),
        y=alt.Y("lfp:Q"),
        text="countryName:N"
    )

    scatter = (_points + _labels).properties(
        width=680,
        height=440,
        title="Female Labor Force Participation vs GDP per Capita, 2023"
    )
    scatter
    return (scatter,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Afghanistan has the lowest female LFP at 5.2%, while Burundi leads at 80% -- a 15x gap driven by cultural and institutional factors, not income alone
        - Middle East and North Africa cluster at the bottom: Iraq (10.9%), Iran (14.1%), Algeria (14.3%), and Jordan (15.9%) all fall below 16%
        - Sub-Saharan African countries dominate the upper-left quadrant, with participation rates of 55-80% despite GDP per capita under $3,000
        - The U-shape is visible: high LFP in poor agrarian economies, a dip in middle-income countries, and recovery in wealthy nations like Iceland (70.4%) and Canada (61.1%)
        """
    )
    return


if __name__ == "__main__":
    app.run()
