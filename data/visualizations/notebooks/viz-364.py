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
        # Terrestrial Protected Areas -- Methodology

        Slope chart comparing 2013 vs 2022 protected land area for countries with
        significant expansions. Source: World Bank ER.LND.PTLD.ZS
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--ER-LND-PTLD-ZS.json"
    raw = json.loads(dataset_path.read_text())
    data = raw["data"]
    print(f"Loaded {len(data)} data points")
    return data, raw


@app.cell
def _(data, json):
    exclude_kw = ["World","income","OECD","Euro","IDA","IBRD","dividend","poor","states",
                  "excluding","Blend","Arab","Africa","Asia","Latin","North America",
                  "Pacific","Caribbean","Central","Eastern","Western","Southern","Northern",
                  "Middle","Least","Sub-Saharan","classification","&"]
    def is_country(name): return not any(kw.lower() in name.lower() for kw in exclude_kw)

    yr2013 = {p["countryName"]: round(p["value"], 1) for p in data if p["year"] == 2013 and p["value"] and p["value"] > 0 and is_country(p["countryName"])}
    yr2022 = {p["countryName"]: round(p["value"], 1) for p in data if p["year"] == 2022 and p["value"] and p["value"] > 0 and is_country(p["countryName"])}

    common = set(yr2013.keys()) & set(yr2022.keys())
    rows = sorted([(n, yr2013[n], yr2022[n], yr2022[n] - yr2013[n]) for n in common], key=lambda x: -x[3])
    # Top 20 by increase + some high-stable countries
    chart_data = [{"n": n, "a": a, "b": b} for n, a, b, _ in rows[:20]]
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, common, rows, yr2013, yr2022


if __name__ == "__main__":
    app.run()
