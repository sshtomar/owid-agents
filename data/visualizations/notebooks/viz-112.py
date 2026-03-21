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
        # The Mobile Revolution: From Zero to Ubiquity

        Mobile cellular subscriptions per 100 people for 9 countries from 1990 to 2023, showing how the mobile phone went from a Finnish novelty to a globally ubiquitous technology in just three decades.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **Mobile Cellular Subscriptions (per 100 people)** (World Bank)
  Indicator: IT.CEL.SETS.P2
  Source: [https://data.worldbank.org/indicator/IT.CEL.SETS.P2](https://data.worldbank.org/indicator/IT.CEL.SETS.P2)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--IT-CEL-SETS-P2.json"
    try:
        _text = _path.read_text()
    except AttributeError:
        _text = urllib.request.urlopen(str(_path)).read().decode()
    _raw = json.loads(_text)
    meta_0 = _raw["meta"]
    df_0 = pd.DataFrame(_raw["data"])
    df_0 = df_0.dropna(subset=["value"])
    mo.md(f"**{meta_0['title']}** -- {len(df_0)} rows, {df_0['countryName'].nunique()} entities, {df_0['year'].min()}--{df_0['year'].max()}")
    mo.ui.table(df_0.head(20))
    return (df_0, meta_0)


@app.cell
def _(mo):
    mo.md(
        """
        ## Transformation

        We select 9 countries that illustrate different phases of the mobile revolution: early adopters (Finland, Italy), technology leaders (Japan, South Korea), rapid catch-up economies (China, Kenya, Bangladesh), the massive-scale case (India), and a late starter (Ethiopia). We filter to 1990 onward and remove null values.
        """
    )
    return


@app.cell
def _(df_0, pd):
    _target_codes = {
        "FI": "Finland",
        "IT": "Italy",
        "JP": "Japan",
        "KR": "South Korea",
        "CN": "China",
        "IN": "India",
        "KE": "Kenya",
        "BD": "Bangladesh",
        "ET": "Ethiopia",
    }

    _filtered = df_0[
        (df_0["country"].isin(_target_codes.keys())) & (df_0["year"] >= 1990)
    ].copy()
    _filtered["countryLabel"] = _filtered["country"].map(_target_codes)

    transformed = _filtered[["countryLabel", "year", "value"]].rename(
        columns={"countryLabel": "country"}
    ).sort_values(["country", "year"]).reset_index(drop=True)

    transformed
    return (transformed,)


@app.cell
def _(transformed, alt, mo):
    _order = [
        "Japan", "South Korea", "Italy", "Finland", "China",
        "Kenya", "Bangladesh", "India", "Ethiopia"
    ]
    _colors = [
        "#dc2626", "#ea580c", "#7c3aed", "#2563eb", "#ca8a04",
        "#0d9488", "#0891b2", "#16a34a", "#6b7280"
    ]

    _base = alt.Chart(transformed).encode(
        x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
        y=alt.Y("value:Q", title="Subscriptions per 100 people"),
        color=alt.Color(
            "country:N",
            title="Country",
            sort=_order,
            scale=alt.Scale(domain=_order, range=_colors),
        ),
    )

    _lines = _base.mark_line(strokeWidth=2)

    _rule = alt.Chart(pd.DataFrame({"y": [100]})).mark_rule(
        strokeDash=[4, 4], color="#e2e8f0"
    ).encode(y="y:Q")

    _chart = (_rule + _lines).properties(
        width=640,
        height=420,
        title="Mobile Cellular Subscriptions per 100 People (1990-2023)"
    )

    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - Finland was the early leader with 5 subscriptions per 100 people in 1990 when most countries had zero
        - Japan now leads at 178 per 100, meaning the average person holds nearly two subscriptions
        - Kenya went from near-zero in 2000 to 121 per 100 in 2023, leapfrogging landline infrastructure entirely
        - India plateaued around 80 per 100 -- lower penetration in a country of 1.4 billion still means over a billion subscriptions
        - Ethiopia remains the furthest behind at 57 per 100, but is among the fastest-growing on the chart
        """
    )
    return


if __name__ == "__main__":
    app.run()
