import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import json
    from pathlib import Path
    return json, mo, Path


@app.cell
def _(mo):
    mo.md(
        """
        # The Factory Shift -- Methodology

        Manufacturing value added as % of GDP, comparing 1995 to 2022.
        Source: World Bank NV.IND.MANF.ZS.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NV-IND-MANF-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    countries = {}
    for pt in data:
        c = pt["countryName"]
        if c not in countries:
            countries[c] = {}
        if pt["value"] is not None and pt["value"] > 0:
            countries[c][str(pt["year"])] = round(pt["value"], 1)

    selected = [
        ("Cambodia", "Cambodia"), ("Bangladesh", "Bangladesh"),
        ("Iran, Islamic Rep.", "Iran"), ("Korea, Rep.", "Korea"),
        ("Indonesia", "Indonesia"), ("Japan", "Japan"),
        ("Czechia", "Czechia"), ("Germany", "Germany"),
        ("Austria", "Austria"), ("Finland", "Finland"),
        ("India", "India"), ("Hungary", "Hungary"),
    ]
    chart_data = []
    for c_key, c_label in selected:
        if c_key in countries:
            a = countries[c_key].get("1995")
            b = countries[c_key].get("2022")
            if a and b:
                chart_data.append({"n": c_label, "a": a, "b": b})
    chart_data.sort(key=lambda x: -x["b"])
    print(f"Chart data: {len(chart_data)} countries")
    for d in chart_data:
        print(f"  {d['n']}: {d['a']}% -> {d['b']}% ({d['b']-d['a']:+.1f})")
    return chart_data, countries, selected


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart -- compares two time points, color encodes direction
        - **Year selection**: 1995 (post-transition baseline) vs 2022 (latest available)
        - **Color**: Green tones for rising, warm tones for declining
        - **Key insight**: Cambodia surged from 9% to 27%; Japan/Finland declined;
          Korea held steady as a manufacturing champion
        """
    )
    return


if __name__ == "__main__":
    app.run()
