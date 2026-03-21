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
        # The Green Revolution: Who Benefited, Who Was Left Behind

        A line chart tracking cereal yield (kg per hectare) from 1961 to 2023 across 8 countries, showing how high-yield crop varieties and modern farming techniques transformed agricultural productivity in Asia and Latin America while parts of Sub-Saharan Africa lagged behind.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Cereal Yield (kg per hectare)** (World Bank)
  Cereal yield, measured as kilograms per hectare of harvested land, includes wheat, rice, maize, barley, oats, rye, millet, sorghum, buckwheat, and mixed grains.
  Source: [https://data.worldbank.org/indicator/AG.YLD.CREL.KG](https://data.worldbank.org/indicator/AG.YLD.CREL.KG)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--AG-YLD-CREL-KG.json"
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

        Filter to 8 countries that tell the Green Revolution story: Japan and France (already high yield in 1961), China and India (dramatic gains from the 1960s onward), Indonesia (major beneficiary of rice varieties), Brazil (later agricultural surge), and Ethiopia and Kenya (Sub-Saharan Africa, relatively stagnant until recently).
        """
    )
    return


@app.cell
def _(df_0, pd):
    _target_countries = ["JP", "FR", "CN", "IN", "ID", "BR", "ET", "KE"]
    selected = df_0[df_0["country"].isin(_target_countries)].copy()
    selected = selected.sort_values(["country", "year"]).reset_index(drop=True)
    selected["value_rounded"] = selected["value"].round(0).astype(int)
    selected
    return (selected,)


@app.cell
def _(selected, alt, mo):
    _color_scale = alt.Scale(
        domain=["France", "Japan", "China", "Indonesia", "Brazil", "India", "Ethiopia", "Kenya"],
        range=["#2563eb", "#7c3aed", "#dc2626", "#059669", "#d97706", "#ea580c", "#64748b", "#94a3b8"],
    )

    _lines = (
        alt.Chart(selected)
        .mark_line(strokeWidth=2)
        .encode(
            x=alt.X("year:Q", title=None, scale=alt.Scale(domain=[1961, 2023])),
            y=alt.Y("value_rounded:Q", title="Cereal yield (kg per hectare)", scale=alt.Scale(domain=[0, 8000])),
            color=alt.Color("countryName:N", title="Country", scale=_color_scale),
            tooltip=["countryName:N", "year:Q", "value_rounded:Q"],
        )
    )

    _endpoint_df = selected.loc[selected.groupby("countryName")["year"].idxmax()]

    _labels = (
        alt.Chart(_endpoint_df)
        .mark_text(align="left", dx=6, fontSize=11, fontWeight="bold")
        .encode(
            x="year:Q",
            y="value_rounded:Q",
            text=alt.Text("countryName:N"),
            color=alt.Color("countryName:N", scale=_color_scale, legend=None),
        )
    )

    _annotation = (
        alt.Chart(pd.DataFrame({"x": [1966]}))
        .mark_rule(strokeDash=[4, 3], stroke="#cbd5e1")
        .encode(x="x:Q")
    )

    _chart = (
        (_annotation + _lines + _labels)
        .properties(
            width=700,
            height=420,
            title="The Green Revolution: Who Benefited, Who Was Left Behind",
        )
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - China increased cereal yields over 5x from 1,193 to 6,418 kg/ha, the most dramatic transformation among major countries
        - Indonesia nearly quadrupled yields from 1,542 to 5,829 kg/ha, driven by high-yield rice varieties from IRRI
        - Kenya's cereal yield in 2023 (1,758 kg/ha) is barely above India's 1961 starting point (947 kg/ha), illustrating the divergence
        - Brazil's surge came later than Asia's, accelerating from the 1990s onward with cerrado agriculture modernization
        - France and Japan started high and plateaued, suggesting diminishing returns at the productivity frontier
        - Ethiopia shows a recent uptick from roughly 1,100 in the early 2000s to 2,864 by 2023, a sign the Green Revolution may finally be reaching East Africa
        """
    )
    return


if __name__ == "__main__":
    app.run()
