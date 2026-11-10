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
        # Electricity Production from Oil Sources — Methodology

        Slope chart comparing countries' oil share of electricity generation from 1990 to latest year.
        Source dataset: wb--EG-ELC-PETR-ZS
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--EG-ELC-PETR-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    country_data = {}
    for p in data:
        if p["value"] is None:
            continue
        cn = p["countryName"]
        yr = p["year"]
        country_data.setdefault(cn, {})[yr] = p["value"]

    skip_words = ["income","Africa","Asia","Europe","America","World","OECD","dividend","Arab","states","IDA","IBRD","South","North","East","West","Central","Caribbean","Euro area","European","Latin","Pacific","Middle","Gulf","Fragility"]
    result = {}
    for k, v in country_data.items():
        if any(w in k for w in skip_words):
            continue
        if 1990 in v:
            later_yrs = [yr for yr in v if yr >= 2019]
            if later_yrs:
                latest_yr = max(later_yrs)
                result[k] = {"a": round(v[1990], 1), "b": round(v[latest_yr], 1), "yr": latest_yr}

    interesting = {k: v for k, v in result.items() if v["a"] > 15 or v["b"] > 15}
    top = sorted(interesting.items(), key=lambda x: x[1]["a"], reverse=True)[:25]
    chart_data = [{"n": n, "a": v["a"], "b": v["b"]} for n, v in top]
    print(f"Countries selected: {len(chart_data)}")
    changes = [v["b"] - v["a"] for v in result.values() if v["a"] > 15]
    print(f"Avg change for high-oil countries: {sum(changes)/len(changes):.1f}pp")
    return chart_data, country_data, interesting, result, top


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Slope chart — before/after at two distinct time points
        - **Year selection**: 1990 (early data) vs most recent year 2019-2024
        - **Country selection**: Countries where oil accounted for >15% in either 1990 or latest
        - **Color**: By magnitude of reduction (deep green = dramatic shift away from oil)
        - **Highlights**: Jordan cut from 88% to 3%; Italy and Indonesia nearly eliminated oil electricity
        - **Stayers**: Chad and Cuba still rely on oil for >80% of electricity
        """
    )
    return


@app.cell
def _(json, chart_data):
    print(json.dumps(chart_data, separators=(",", ":")))
    return


if __name__ == "__main__":
    app.run()
