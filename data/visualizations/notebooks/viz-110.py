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
        # Saving Children: Under-5 Mortality, 2000 vs 2020

        A slope chart comparing under-5 mortality rates (deaths per 1,000 live births) between 2000 and 2020 across 18 countries. The chart highlights dramatic declines in child mortality across much of the developing world, alongside rare reversals in small island nations.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Under-5 Mortality Rate (per 1,000 live births)** (World Bank)
          Mortality rate, under-5 (per 1,000 live births) from World Bank
          Source: [https://data.worldbank.org/indicator/SH.DYN.MORT](https://data.worldbank.org/indicator/SH.DYN.MORT)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--SH-DYN-MORT.json"
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

        Filter to years 2000 and 2020, keeping only real countries (excluding World Bank aggregates).
        Select 18 countries that illustrate dramatic improvements, moderate progress, and surprising reversals.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _selected_codes = [
        "AO", "TD", "GW", "BF", "ET", "KH", "SZ", "IN",
        "GH", "KE", "BD", "BW", "BO", "ID", "CN", "BR", "FJ", "DM"
    ]
    _filtered = df_0[
        (df_0["year"].isin([2000, 2020])) &
        (df_0["country"].isin(_selected_codes))
    ].copy()

    _pivot = _filtered.pivot_table(
        index=["country", "countryName"],
        columns="year",
        values="value"
    ).reset_index()
    _pivot.columns = ["country", "countryName", "y2000", "y2020"]
    _pivot = _pivot.dropna(subset=["y2000", "y2020"])
    _pivot["change"] = _pivot["y2020"] - _pivot["y2000"]
    _pivot["pct_change"] = (_pivot["change"] / _pivot["y2000"] * 100).round(1)

    def classify(row):
        if row["change"] > 0:
            return "reversal"
        elif abs(row["pct_change"]) >= 60:
            return "dramatic"
        else:
            return "moderate"

    _pivot["group"] = _pivot.apply(classify, axis=1)
    transformed = _pivot.sort_values("y2000", ascending=False).copy()
    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, pd, mo):
    _start = transformed[["countryName", "y2000", "group"]].rename(
        columns={"y2000": "value"}
    )
    _start["year"] = "2000"
    _end = transformed[["countryName", "y2020", "group"]].rename(
        columns={"y2020": "value"}
    )
    _end["year"] = "2020"
    _plot_df = pd.concat([_start, _end], ignore_index=True)

    _color_scale = alt.Scale(
        domain=["dramatic", "moderate", "reversal"],
        range=["#2563eb", "#64748b", "#ef4444"]
    )

    _lines = (
        alt.Chart(_plot_df)
        .mark_line(strokeWidth=2, opacity=0.7)
        .encode(
            x=alt.X("year:N", title=None, sort=["2000", "2020"]),
            y=alt.Y("value:Q", title="Deaths per 1,000 live births", scale=alt.Scale(domain=[0, 220])),
            detail="countryName:N",
            color=alt.Color("group:N", title="Change type", scale=_color_scale),
            tooltip=["countryName", "year", "value"],
        )
    )
    _points = (
        alt.Chart(_plot_df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("year:N", sort=["2000", "2020"]),
            y=alt.Y("value:Q"),
            color=alt.Color("group:N", scale=_color_scale),
            tooltip=["countryName", "year", "value"],
        )
    )
    _labels_left = (
        alt.Chart(_plot_df[_plot_df["year"] == "2000"])
        .mark_text(align="right", dx=-8, fontSize=10, fontWeight=600)
        .encode(
            x=alt.X("year:N", sort=["2000", "2020"]),
            y=alt.Y("value:Q"),
            text=alt.Text("countryName:N"),
            color=alt.Color("group:N", scale=_color_scale),
        )
    )
    _labels_right = (
        alt.Chart(_plot_df[_plot_df["year"] == "2020"])
        .mark_text(align="left", dx=8, fontSize=10, fontWeight=600)
        .encode(
            x=alt.X("year:N", sort=["2000", "2020"]),
            y=alt.Y("value:Q"),
            text=alt.Text("countryName:N"),
            color=alt.Color("group:N", scale=_color_scale),
        )
    )

    _chart = (_lines + _points + _labels_left + _labels_right).properties(
        width=600,
        height=500,
        title="Under-5 Mortality Rate: 2000 vs 2020"
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Angola saw the single largest absolute decline, dropping from 203 to 71.6 deaths per 1,000 live births (-131 deaths)
        - Cambodia achieved a 76% reduction, from 106 to just 26 deaths -- one of the steepest percentage drops globally
        - China reached near-developed-nation levels at 7.5 per 1,000, down from 36.7 in 2000
        - Chad still has the highest rate (111 per 1,000) despite a substantial decline from 184
        - Dominica and Fiji are rare reversals where under-5 mortality actually increased between 2000 and 2020
        """
    )
    return


if __name__ == "__main__":
    app.run()
