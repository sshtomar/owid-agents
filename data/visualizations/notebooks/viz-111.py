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
        # The Carbon Shift: Who Drives Global CO2 Emissions?

        CO2 emissions from fuel combustion (millions of tonnes) for the eight largest emitters, 2000 to 2022. China overtook the United States around 2006 and now emits more than twice as much, while India has tripled its output.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Data Sources

        - **CO2 Emissions from Fuel Combustion (millions of tonnes)** (UN SDG)
  Carbon dioxide emissions from fuel combustion, SDG indicator 9.4.1
  Source: [https://unstats.un.org/sdgs/dataportal/database](https://unstats.un.org/sdgs/dataportal/database)
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
    _path = mo.notebook_location() / "public" / "catalog" / "datasets" / "sdg--9-4-1--EN_ATM_CO2.json"
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

        The dataset contains two interleaved sub-indicators per country. We separate them by parity (even vs odd years) and select the series with higher average values as the total emissions series. We then pick the top 8 emitters and interpolate to a common biennial time axis (2000-2022).
        """
    )
    return


@app.cell
def _(df_0, pd):
    # Regional aggregates to exclude
    _aggregates = {
        "Africa", "Americas", "Asia", "Europe", "Oceania", "World",
        "Australia and New Zealand", "Caribbean", "Caucasus and Central Asia",
        "Central America", "Central Asia", "Central and Southern Asia",
        "Developing regions", "Eastern Africa", "Eastern Asia", "Eastern Europe",
        "Eastern and South-Eastern Asia", "Europe and Northern America",
        "Latin America and the Caribbean", "Middle Africa", "Northern Africa",
        "Northern Africa and Western Asia", "Northern America", "Northern Europe",
        "South America", "South-Eastern Asia", "Southern Africa", "Southern Asia",
        "Southern Europe", "Sub-Saharan Africa", "Western Africa", "Western Asia",
        "Western Europe", "Oceania (exc. Australia and New Zealand)",
        "Landlocked developing countries (LLDCs)",
        "Least Developed Countries (LDCs)",
        "Small island developing States (SIDS)",
        "Developed regions (Europe, Cyprus, Israel, Northern America, Japan, Australia & New Zealand)",
        "Other Africa (IEA)", "Other non-OECD Americas",
    }

    _countries = df_0[~df_0["countryName"].isin(_aggregates)].copy()

    # For each country, pick the even/odd parity with higher average
    def _get_totals(group):
        even = group[group["year"] % 2 == 0]
        odd = group[group["year"] % 2 == 1]
        even_avg = even["value"].mean() if len(even) > 0 else 0
        odd_avg = odd["value"].mean() if len(odd) > 0 else 0
        return even if even_avg > odd_avg else odd

    _totals = _countries.groupby("countryName", group_keys=False).apply(_get_totals)
    _ranked = _totals.groupby("countryName")["value"].mean().sort_values(ascending=False)

    top8_names = _ranked.head(8).index.tolist()

    _short = {
        "China": "China",
        "United States of America": "United States",
        "Russian Federation": "Russia",
        "India": "India",
        "Japan": "Japan",
        "Germany": "Germany",
        "Republic of Korea": "South Korea",
        "Canada": "Canada",
    }

    _target_years = list(range(2000, 2024, 2))
    _rows = []
    for name in top8_names:
        sn = _short.get(name, name)
        _sub = _totals[_totals["countryName"] == name].sort_values("year")
        _by_year = dict(zip(_sub["year"], _sub["value"]))
        for y in _target_years:
            if y in _by_year:
                _rows.append({"year": y, "country": sn, "value": round(_by_year[y], 1)})
            else:
                before = [(yr, v) for yr, v in _by_year.items() if yr < y]
                after = [(yr, v) for yr, v in _by_year.items() if yr > y]
                if before and after:
                    b_yr, b_v = max(before)
                    a_yr, a_v = min(after)
                    t = (y - b_yr) / (a_yr - b_yr)
                    _rows.append({"year": y, "country": sn, "value": round(b_v + t * (a_v - b_v), 1)})
                elif before:
                    _rows.append({"year": y, "country": sn, "value": round(max(before)[1], 1)})
                elif after:
                    _rows.append({"year": y, "country": sn, "value": round(min(after)[1], 1)})

    transformed = pd.DataFrame(_rows)
    transformed
    return (transformed, top8_names)


@app.cell
def _(transformed, alt, mo):
    _order = ["China", "United States", "India", "Russia", "Japan", "Germany", "South Korea", "Canada"]
    _colors = ["#E15759", "#4E79A7", "#F28E2B", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7"]

    _chart = (
        alt.Chart(transformed)
        .mark_area()
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="CO2 Emissions (millions of tonnes)", stack="zero"),
            color=alt.Color(
                "country:N",
                title="Country",
                sort=_order,
                scale=alt.Scale(domain=_order, range=_colors),
            ),
            order=alt.Order("_order:Q"),
            tooltip=["country", "year", "value"],
        )
        .transform_calculate(_order="indexof(" + str(_order) + ", datum.country)")
        .properties(width=600, height=400, title="CO2 Emissions from Fuel Combustion by Country (2000-2022)")
    )
    mo.ui.altair_chart(_chart)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Insights

        - China's emissions tripled from ~3,200 to ~10,600 MT between 2000 and 2022, becoming the world's largest emitter
        - The United States decreased emissions by 20%, from ~5,700 to ~4,550 MT, losing its top position around 2006
        - India nearly tripled from ~900 to ~2,500 MT, emerging as the third largest emitter
        - Germany and Japan both reduced emissions by roughly 15-25%, showing progress in decarbonization
        """
    )
    return


if __name__ == "__main__":
    app.run()
