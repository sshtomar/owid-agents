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
        # Natural Resource Rents — Methodology

        Documents the trend lines visualization showing total natural resource
        rents as % of GDP for resource-dependent economies, 2000–2021.
        """
    )
    return


@app.cell
def _(json, mo):
    dataset_path = mo.notebook_location() / "public" / "catalog" / "datasets" / "wb--NY-GDP-TOTL-RT-ZS.json"
    raw = json.loads(dataset_path.read_text())
    meta = raw["meta"]
    data = raw["data"]
    print(f"Loaded {len(data)} data points: {meta['title']}")
    return data, meta, raw


@app.cell
def _(data):
    import re
    country_data = {}
    for pt in data:
        code = pt["country"]
        if re.match(r"^[A-Z]{2}$", code) and pt["value"] is not None:
            cn = pt["countryName"]
            yr = pt["year"]
            if cn not in country_data:
                country_data[cn] = {}
            country_data[cn][yr] = pt["value"]
    focus = ["Iraq", "Congo, Rep.", "Angola", "Kazakhstan", "Azerbaijan", "Canada", "China"]
    for cn in focus:
        if cn in country_data:
            v2000 = round(country_data[cn].get(2000, 0), 1)
            v2021 = round(country_data[cn].get(2021, 0), 1)
            print(f"{cn}: 2000={v2000}%, 2021={v2021}%")
    return cn, code, country_data, focus, pt, re, v2000, v2021, yr


@app.cell
def _(mo):
    mo.md(
        """
        ## Design Rationale

        - **Chart type**: Trend lines — annual data 2000–2021 shows oil-price volatility clearly
        - **Country selection**: High-dependency petrostates (Iraq, Congo, Angola, Kazakhstan, Azerbaijan) + low-dependency for contrast (Canada, China)
        - **Annotations**: Vertical dashed lines at 2009 crash and 2015 oil glut to explain the synchronised dips
        - **Story**: Resource-dependent economies are extremely vulnerable to commodity price shocks; the 2009 and 2015 crashes visible across all lines simultaneously
        """
    )
    return


@app.cell
def _(country_data, focus, json):
    years = list(range(2000, 2022))
    chart_data = []
    for name in focus:
        if name in country_data:
            pts = [{"y": yr, "v": round(country_data[name][yr], 2)} for yr in years if yr in country_data[name]]
            if len(pts) >= 15:
                chart_data.append({"n": name, "pts": pts})
    print(json.dumps(chart_data, separators=(",", ":")))
    return chart_data, name, pts, years, yr


if __name__ == "__main__":
    app.run()
