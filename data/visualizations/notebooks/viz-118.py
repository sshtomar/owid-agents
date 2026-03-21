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
        # The Many Speeds of Globalization

        A line chart tracking trade (exports + imports) as a share of GDP from 1960 to 2024 across 10 countries, revealing how trading hubs, economies that liberalized, protectionist holdouts, and steady traders followed vastly different paths into the global economy.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Trade (% of GDP)** (World Bank)
  Trade is the sum of exports and imports of goods and services measured as a share of gross domestic product.
  Source: [https://data.worldbank.org/indicator/NE.TRD.GNFS.ZS](https://data.worldbank.org/indicator/NE.TRD.GNFS.ZS)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NE-TRD-GNFS-ZS.json"
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

        Filter to 10 countries that tell distinct globalization stories:

        - **Trading hubs**: Hong Kong (re-export entrepot), Ireland (multinational IP routing)
        - **Opened up**: China (post-1978 reforms), India (post-1991 liberalization), South Korea (export-led industrialization)
        - **Inward-looking**: Argentina and Brazil (import substitution, periodic closures)
        - **Steady traders**: Germany (manufacturing exporter), Japan (trade grew slowly), Chile (early liberalizer)
        """
    )
    return


@app.cell
def _(df_0, pd):
    _target_countries = ["HK", "IE", "CN", "IN", "AR", "BR", "DE", "JP", "KR", "CL"]
    _name_map = {
        "HK": "Hong Kong",
        "IE": "Ireland",
        "CN": "China",
        "IN": "India",
        "AR": "Argentina",
        "BR": "Brazil",
        "DE": "Germany",
        "JP": "Japan",
        "KR": "South Korea",
        "CL": "Chile",
    }
    selected = df_0[df_0["country"].isin(_target_countries)].copy()
    selected["label"] = selected["country"].map(_name_map)
    selected["value_rounded"] = selected["value"].round(1)
    selected = selected.sort_values(["country", "year"]).reset_index(drop=True)
    selected
    return (selected,)


@app.cell
def _(selected, alt, pd, mo):
    _countries = [
        "Hong Kong", "Ireland", "China", "India", "South Korea",
        "Argentina", "Brazil", "Germany", "Japan", "Chile",
    ]
    _colors = [
        "#e41a1c", "#ff7f00", "#377eb8", "#4daf4a", "#e7298a",
        "#984ea3", "#a65628", "#333333", "#999999", "#66a61e",
    ]

    _color_scale = alt.Scale(domain=_countries, range=_colors)

    _lines = (
        alt.Chart(selected)
        .mark_line(strokeWidth=1.8)
        .encode(
            x=alt.X("year:Q", title=None, scale=alt.Scale(domain=[1960, 2024])),
            y=alt.Y("value_rounded:Q", title="Trade (% of GDP)", scale=alt.Scale(domain=[0, 400])),
            color=alt.Color("label:N", title="Country", scale=_color_scale),
            tooltip=["label:N", "year:Q", "value_rounded:Q"],
        )
    )

    _endpoint_df = selected.loc[selected.groupby("label")["year"].idxmax()]

    _labels = (
        alt.Chart(_endpoint_df)
        .mark_text(align="left", dx=6, fontSize=11, fontWeight="bold")
        .encode(
            x="year:Q",
            y="value_rounded:Q",
            text=alt.Text("label:N"),
            color=alt.Color("label:N", scale=_color_scale, legend=None),
        )
    )

    _threshold = (
        alt.Chart(pd.DataFrame({"y": [100]}))
        .mark_rule(strokeDash=[4, 3], stroke="#e2e8f0")
        .encode(y="y:Q")
    )

    _chart = (
        (_threshold + _lines + _labels)
        .properties(
            width=750,
            height=460,
            title="The Many Speeds of Globalization",
        )
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Hong Kong trade reached 360% of GDP by 2024, reflecting its role as a re-export hub where goods pass through multiple times
        - Ireland surged from 80% to 246% after the 1990s as multinationals routed intellectual property exports through Dublin
        - China's trade share rose from 5% in 1960 to a peak of about 65% around 2006, then retreated to 37% as its domestic economy matured
        - Argentina and Brazil remain among the most closed large economies, with trade shares of 28% and 36% respectively in 2024
        - South Korea's transformation from 36% in 1970 to 85% today tracks its rise from agricultural economy to semiconductor powerhouse
        - Germany's steady climb from about 40% to 79% reflects its position as Europe's manufacturing backbone
        - Chile liberalized early under Pinochet-era reforms in the 1970s and has maintained trade openness around 55--65% since the 1990s
        """
    )
    return


if __name__ == "__main__":
    app.run()
